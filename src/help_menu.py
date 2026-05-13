import pygame
from src.menu_sprites import Box, Picture, Button, Text
from typing import Any


class HelpMenu:
    """Display the help screen with a return option."""

    def __init__(self, engine: Any, root_menu: Any) -> None:
        """Initialize help menu assets.

        Args:
            engine: Engine instance for screen sizing and rendering.
            root_menu: Parent menu for switching views.
        """
        self.root_menu = root_menu
        self.engine = engine
        self.assets: Any = pygame.sprite.Group()
        pixelmania = pygame.font.Font("./assets/Pixelmania.ttf", 15)

        self.assets.add(
            Box(
                self.engine.screen_width * 0.98,
                self.engine.screen_height * 0.98,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height // 2,
                ),
                200,
            )
        )
        return_button = Button(
            "RETURN",
            pixelmania,
            (
                self.engine.screen_width // 2,
                self.engine.screen_height * 0.1,
            ),
            1,
            "yellow",
        )
        self.assets.add(return_button)

        line_spacing = self.engine.screen_height * 0.05
        self.assets.add(
            Text(
                "CONTROLS",
                "yellow",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20,
                ),
            )
        )

        self.assets.add(
            Text(
                "↑ UP - Move Up",
                "white",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing,
                ),
            )
        )

        self.assets.add(
            Text(
                "↓ DOWN - Move Down",
                "white",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing * 2,
                ),
            )
        )

        self.assets.add(
            Text(
                "← LEFT - Move Left",
                "white",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing * 3,
                ),
            )
        )

        self.assets.add(
            Text(
                "→ RIGHT - Move Right",
                "white",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing * 4,
                ),
            )
        )

        self.assets.add(
            Text(
                "ENTER - Select in Menus",
                "white",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing * 5,
                ),
            )
        )

        self.assets.add(
            Text(
                "ESC - Pause and Resume Game",
                "white",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing * 6,
                ),
            )
        )

        self.assets.add(
            Text(
                "CHEAT CODES",
                "red",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing * 8,
                ),
            )
        )

        self.assets.add(
            Text(
                "I - Invincibility",
                "white",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing * 9,
                ),
            )
        )

        self.assets.add(
            Text(
                "L - Skip Level",
                "white",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing * 10,
                ),
            )
        )

        self.assets.add(
            Text(
                "E - Extra Life",
                "white",
                self.root_menu.montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.20 + line_spacing * 11,
                ),
            )
        )

        self.assets.add(
            Picture(
                "right_selector",
                "./assets/pacman_right.png",
                20,
                20,
                (
                    int(return_button.rect.midright[0] + 15),
                    int(return_button.rect.midright[1]),
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
                    int(return_button.rect.midleft[0] - 15),
                    int(return_button.rect.midleft[1]),
                ),
            )
        )

    def draw(self) -> None:
        """Draw the help menu assets."""
        self.assets.draw(self.engine.screen)

    def show(
        self,
    ) -> None:
        """Render the help menu to the screen."""
        self.assets.draw(self.engine.screen)

    def event(self, event: pygame.event.Event) -> None:
        """Handle input events for the help menu.

        Args:
            event: Pygame event to process.
        """
        if event.key == pygame.K_RETURN:
            self.root_menu.switch_menu("welcome_menu")
