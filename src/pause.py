"""Pause menu overlay displayed during gameplay."""

import pygame
from typing import Any
from src.menu_sprites import Box, Text, Button, Picture


class PauseMenu:
    """Render a pause overlay with a return option."""

    def __init__(self, engine: Any) -> None:
        """Initialize pause menu assets.

        Args:
            engine: Engine instance for screen sizing and rendering.
        """
        self.engine = engine
        self.assets: Any = pygame.sprite.Group()
        pixelmania = pygame.font.Font("./assets/Pixelmania.ttf", 15)
        self.assets.add(
            Box(
                self.engine.screen_width * 3,
                self.engine.screen_height * 3,
                (0, 0),
                200,
            )
        )
        self.assets.add(
            Text(
                "PAUSED",
                "yellow",
                pixelmania,
                (
                    self.engine.screen_width // 2,
                    (self.engine.screen_height * 0.48) - 50,
                ),
            )
        )
        return_button = Button(
            "RETURN",
            pixelmania,
            (
                self.engine.screen_width // 2,
                self.engine.screen_height * 0.48,
            ),
            1,
            "white",
        )
        self.assets.add(return_button)
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
        """Draw the pause overlay."""
        self.assets.draw(self.engine.screen)
