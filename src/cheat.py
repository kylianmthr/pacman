"""Cheat input handler for gameplay shortcuts."""

import pygame
from typing import Any


class Cheats:
    """Toggle gameplay cheats such as invisibility and speed."""

    def __init__(self, game: Any) -> None:
        """Initialize cheat state for a game instance.

        Args:
            game: Game instance to manipulate.
        """
        self.game = game
        self.invisibility = False
        self.speed = 1

    def event(self, evt: pygame.event.Event) -> None:
        """Handle cheat key inputs.

        Args:
            evt: Pygame event to process.
        """
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_i:
                self.invisibility = not self.invisibility
            elif evt.key == pygame.K_s:
                if self.speed == 1:
                    self.speed = 2
                else:
                    self.speed = 1
            elif evt.key == pygame.K_l:
                self.game.engine.next_level()
            elif evt.key == pygame.K_e:
                self.game.lives += 1
