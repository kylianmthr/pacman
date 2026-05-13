"""Leaderboard menu display and navigation."""

import pygame
from pygame.math import Vector2
from typing import Any, cast
from src.menu_sprites import Button, Picture, Text, TextFromRight, TextFromLeft
from src.wall import Wall


class LeaderBoardMenu:
    """Render the leaderboard screen and return navigation."""

    def __init__(self, engine: Any, root_menu: Any) -> None:
        """Initialize the leaderboard menu assets.

        Args:
            engine: Engine instance for rendering and state access.
            root_menu: Parent menu for shared fonts.
        """
        self.root_menu = root_menu
        self.engine = engine
        self.assets: Any = pygame.sprite.Group()
        self.buttons: list[Button] = []
        self.button_idx = 0
        self.cursors_map: dict[str, dict[str, Vector2]] = {}
        self.create_static_surfaces()

    def show(
        self,
    ) -> None:
        """Draw the leaderboard menu to the screen."""
        self.engine.screen.fill("black")
        self.assets.draw(self.engine.screen)

    def update_sprite(
        self, sprite: Any, coordinates: tuple[float, float]
    ) -> None:
        """Update the sprite position.

        Args:
            sprite: Sprite instance to move.
            coordinates: New center coordinates.
        """
        sprite.rect = sprite.image.get_rect(center=coordinates)

    def create_static_surfaces(self) -> None:
        """Create static UI elements for the leaderboard."""
        self.assets.add(
            Text(
                "1              9",
                "yellow",
                self.root_menu.pacfont,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.1,
                ),
            )
        )
        self.assets.add(
            Text(
                "PACMAN",
                "yellow",
                self.root_menu.pacfont,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.1,
                ),
            )
        )
        self.assets.add(
            Text(
                "22222222222222",
                "yellow",
                self.root_menu.pacfont,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.1 + 40,
                ),
            )
        )

        self.assets.add(
            Button(
                "RETURN",
                self.root_menu.pixelmania,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.27,
                ),
                1,
                "yellow",
            )
        )
        self.buttons = [
            button for button in self.assets if isinstance(button, Button)
        ]
        self.cursors_map = {
            button.name: {
                "left": Vector2(button.rect.midleft),
                "right": Vector2(button.rect.midright),
            }
            for button in self.buttons
        }
        self.assets.add(
            Picture(
                "right_selector",
                "./assets/pacman_right.png",
                20,
                20,
                (
                    int(
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "right"
                        ].x
                        + 15
                    ),
                    int(
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "right"
                        ].y
                    ),
                ),
            )
        )
        self.assets.add(
            Picture(
                "left_selector",
                "./assets/pacman_left.png",
                20,
                20,
                (
                    int(
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "left"
                        ].x
                        - 15
                    ),
                    int(
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "left"
                        ].y
                    ),
                ),
            )
        )
        self.assets.add(
            Wall(5, self.engine.screen_height, (0, 0), "white", "frame")
        )
        self.assets.add(
            Wall(self.engine.screen_width, 5, (0, 0), "white", "frame")
        )
        self.assets.add(
            Wall(
                self.engine.screen_width,
                5,
                (0, self.engine.screen_height - 5),
                "white",
                "frame",
            )
        )
        self.assets.add(
            Wall(
                5,
                self.engine.screen_height,
                (self.engine.screen_width - 5, 0),
                "white",
                "frame",
            )
        )

    def update_leaderboard_surfaces(self) -> None:
        """Refresh leaderboard entries and frame colors."""
        for asset in self.assets:
            asset.kill()
        self.create_static_surfaces()
        self.engine.leaderboard.data_retriever()
        coordinate_player_name = Vector2(
            self.engine.screen_width * 0.05, self.engine.screen_height * 0.3
        )
        coordinate_player_score = Vector2(
            self.engine.screen_width * 0.95, self.engine.screen_height * 0.3
        )
        for player in self.engine.leaderboard.high_scores.best_players:
            if player.score > 0:
                coordinate_player_name += Vector2(0, 28)
                coordinate_player_score += Vector2(0, 28)
                self.assets.add(
                    TextFromLeft(
                        f"{player.name}",
                        "yellow",
                        self.root_menu.superfunnel,
                        (
                            int(coordinate_player_name.x),
                            int(coordinate_player_name.y),
                        ),
                    )
                )
                if player.score > 9999999999999:
                    self.assets.add(
                        TextFromRight(
                            "Game finished",
                            "yellow",
                            self.root_menu.karma_future,
                            (
                                int(coordinate_player_score.x),
                                int(coordinate_player_score.y),
                            ),
                        )
                    )
                else:
                    self.assets.add(
                        TextFromRight(
                            f"{player.score}",
                            "yellow",
                            self.root_menu.karma_future,
                            (
                                int(coordinate_player_score.x),
                                int(coordinate_player_score.y),
                            ),
                        )
                    )
        frames = [
            frame
            for frame in self.assets
            if cast(Any, frame).name == "frame"
        ]
        for frame in frames:
            frame.image.fill(self.engine.color)

    def event(self, event: pygame.event.Event) -> None:
        """Handle input events for the leaderboard.

        Args:
            event: Pygame event to process.
        """
        if event.key == pygame.K_RETURN:
            self.root_menu.switch_menu("welcome_menu")
