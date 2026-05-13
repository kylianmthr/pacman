"""End-of-game menu for name entry and score display."""

import pygame
from typing import Any

from src.menu_sprites import Text
from src.models import Player


class EndOfGameMenu:
    """Render the game over or game finished screens."""

    def __init__(self, engine: Any, type: str, root_menu: Any) -> None:
        """Initialize the end-of-game menu assets.

        Args:
            engine: Engine instance for rendering and state access.
            type: Menu type ("game_over" or "game_finished").
            root_menu: Parent menu for shared fonts.
        """
        self.root_menu = root_menu
        self.player_name = "|"
        self.player_name_display: Text | None = None
        self.type = type
        self.engine = engine
        self.assets: Any = pygame.sprite.Group()
        self.create_static_surfaces()

    def create_static_surfaces(self) -> None:
        """Create static title and input prompt surfaces."""
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

        if self.type == "game_over":
            self.assets.add(
                Text(
                    "GAME OVER",
                    "yellow",
                    self.root_menu.pacfont,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.4,
                    ),
                ),
            )
        elif self.type == "game_finished":
            self.assets.add(
                Text(
                    "GAME FINISHED",
                    "yellow",
                    self.root_menu.pacfont,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.4,
                    ),
                ),
                Text(
                    "WELL DONE !",
                    "yellow",
                    self.root_menu.montserrat,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.5,
                    ),
                ),
            )
        self.player_name_display = Text(
            self.player_name,
            "black",
            self.root_menu.montserrat,
            (
                self.engine.screen_width // 2,
                self.engine.screen_height * 0.65 + 60,
            ),
        )
        self.assets.add(self.player_name_display)
        self.assets.add(
            Text(
                "ENTER YOUR NAME",
                "yellow",
                self.root_menu.pixelmania,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.65,
                ),
            ),
        )

    def display_score(self) -> None:
        """Render the player's score on the menu."""
        if self.engine.score > 9999999999999:
            self.assets.add(
                Text(
                    "Maximum score",
                    "yellow",
                    self.root_menu.montserrat,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.65 + 30,
                    ),
                ),
            )
        else:
            self.assets.add(
                Text(
                    f"{self.engine.score} points",
                    "yellow",
                    self.root_menu.montserrat,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.65 + 30,
                    ),
                ),
            )

    def show(
        self,
    ) -> None:
        """Show the end-of-game menu and refresh text."""

        self.engine.screen.fill("black")
        self.write_player_score()
        self.assets.draw(self.engine.screen)

    def write_player_score(self) -> None:
        """Update the player name text surface."""
        if self.player_name_display is None:
            return
        self.player_name_display.image = self.root_menu.montserrat.render(
            self.player_name, True, "yellow", None
        )
        self.player_name_display.rect = (
            self.player_name_display.image.get_rect(
                center=self.player_name_display.coordinates
            )
        )

    def event(self, event: pygame.event.Event) -> None:
        """Handle player name input and submission.

        Args:
            event: Pygame event to process.
        """
        if (event.unicode.isalnum() or event.unicode == " ") and len(
            self.player_name
        ) < 11:
            self.player_name = (
                self.player_name[: len(self.player_name) - 1]
                + event.unicode
                + "|"
            )
            self.write_player_score()
            self.show()
        if event.key == 8 and len(self.player_name) > 0:
            self.player_name = (
                self.player_name[: len(self.player_name) - 2] + "|"
            )
        if event.key == pygame.K_RETURN and len(self.player_name) > 0:
            self.engine.leaderboard.rank_player(
                Player(
                    name=self.player_name[: len(self.player_name) - 1],
                    score=self.engine.score,
                )
            )
            self.engine.running = False
