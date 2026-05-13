"""Welcome menu with navigation and settings toggles."""

import pygame
from pygame import mixer
from pygame.math import Vector2
from typing import Any, cast
from src.menu_sprites import Button, Picture
from src.wall import Wall


class WelcomeMenu:
    """Display the main menu and handle selections."""

    def __init__(self, engine: Any, root_menu: Any) -> None:
        """Initialize the welcome menu and static assets.

        Args:
            engine: Engine instance for rendering and state updates.
            root_menu: Parent menu for switching views.
        """
        self.root_menu = root_menu
        self.engine = engine
        self.assets: Any = pygame.sprite.Group()
        self.music_state = "./assets/music_on.png"
        self.frame_color = "white"
        self.buttons: list[Button] = []
        self.button_idx = 0
        self.cursors_map: dict[str, dict[str, Vector2]] = {}
        self.create_static_surfaces()

    def show(self) -> None:
        """Render the welcome menu to the screen."""
        self.engine.screen.fill("black")
        self.assets.draw(self.engine.screen)

    def update_sprite_coordinate(
        self, sprite: Any, coordinates: tuple[float, ...]
    ) -> None:
        """Move a sprite to the specified coordinates.

        Args:
            sprite: Sprite instance to update.
            coordinates: New center coordinates.
        """
        sprite.rect = sprite.image.get_rect(center=coordinates)

    def update_sprite_file_path(self, sprite: Any, path: str) -> None:
        """Update the music icon sprite based on the current state.

        Args:
            sprite: Sprite instance to update.
            path: Path to the new image asset (unused; uses music_state).
        """
        sprite.image = pygame.image.load(self.music_state)
        sprite.image = pygame.transform.smoothscale(
            sprite.image, (sprite.scale_width, sprite.scale_height)
        )
        sprite.rect = sprite.image.get_rect(center=sprite.coordinates)

    def update_cursor(self) -> None:
        """Reposition the selection cursor based on the active button."""
        for sprite in self.assets:
            if cast(Any, sprite).name == "right_selector":
                self.update_sprite_coordinate(
                    cast(Any, sprite),
                    tuple(
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "right"
                        ]
                        + Vector2(15, 0)
                    ),
                )
            if cast(Any, sprite).name == "left_selector":
                self.update_sprite_coordinate(
                    cast(Any, sprite),
                    tuple(
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "left"
                        ]
                        + Vector2(-15, 0)
                    ),
                )

    def item_selection(self, move: int) -> None:
        """Move the selection cursor within the button list.

        Args:
            move: Directional offset for the selection index.
        """
        if len(self.buttons) > 0:
            self.button_idx = (self.button_idx + move) % len(self.buttons)
        self.update_cursor()

    def create_static_surfaces(self) -> None:
        """Create static sprites for the welcome menu layout."""
        self.assets.add(
            Picture(
                "logo",
                "./assets/logo.png",
                350,
                200,
                (
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.15,
                    )
                ),
            )
        )
        self.assets.add(
            Button(
                "START",
                self.root_menu.pixelmania,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.35,
                ),
                1,
                "yellow",
            )
        )
        self.assets.add(
            Button(
                "LEADERBOARD",
                self.root_menu.pixelmania,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.35 + 50,
                ),
                2,
                "yellow",
            )
        )
        self.assets.add(
            Button(
                "HELP",
                self.root_menu.pixelmania,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.35 + 100,
                ),
                3,
                "yellow",
            )
        )
        self.assets.add(
            Button(
                "EXIT",
                self.root_menu.pixelmania,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.35 + 150,
                ),
                3,
                "yellow",
            )
        )
        self.assets.add(
            Button(
                "music",
                self.music_state,
                (
                    self.engine.screen_width * 0.3,
                    self.engine.screen_height * 0.9,
                ),
                4,
                "",
            )
        )
        self.assets.add(
            Button(
                "color",
                "./assets/color.png",
                (
                    self.engine.screen_width * 0.7,
                    self.engine.screen_height * 0.9,
                ),
                5,
                "",
            )
        )
        self.buttons = [
            button for button in self.assets if isinstance(button, Button)
        ]
        self.buttons.sort(key=lambda button: button.position)
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

    def change_color_frame(self) -> None:
        """Cycle frame color and apply it to walls."""
        frames = [
            frame
            for frame in self.assets
            if cast(Any, frame).name == "frame"
        ]
        colors = [
            "white",
            "blue",
            "red",
            "green",
            "yellow",
            "purple",
            "brown",
            "orange",
        ]
        current = (colors.index(self.engine.color) + 1) % len(colors)
        self.engine.color = colors[current]
        self.engine.change_wall_color()
        for frame in frames:
            frame.image.fill(self.engine.color)

    def event(self, event: pygame.event.Event) -> None:
        """Handle input events for menu navigation and actions.

        Args:
            event: Pygame event to process.
        """
        if event.key == pygame.K_RETURN:
            if self.buttons[self.button_idx].name == "START":
                self.engine.menu_active = False
                if self.engine.music_active:
                    self.engine.music.ghost_sound_effect()
            elif self.buttons[self.button_idx].name == "LEADERBOARD":
                self.root_menu.switch_menu("leaderboard")
            elif self.buttons[self.button_idx].name == "HELP":
                self.root_menu.switch_menu("help_menu")
            elif self.buttons[self.button_idx].name == "EXIT":
                self.engine.running = False
                self.engine.quit = True
            elif self.buttons[self.button_idx].name == "music":
                if self.music_state == "./assets/music_on.png":
                    self.music_state = "./assets/music_off.png"
                elif self.music_state == "./assets/music_off.png":
                    self.music_state = "./assets/music_on.png"
                for sprite in self.assets:
                    if cast(Any, sprite).name == "music":
                        self.update_sprite_file_path(
                            cast(Any, sprite), self.music_state
                        )
                if self.music_state == "./assets/music_on.png":
                    self.engine.music_active = True
                    self.engine.music.start_music()
                else:
                    self.engine.music_active = False
                    mixer.music.stop()
            elif self.buttons[self.button_idx].name == "color":
                self.change_color_frame()
        if event.key in (pygame.K_UP, pygame.K_w):
            self.item_selection(-1)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.item_selection(+1)
