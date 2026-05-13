"""Wall sprite for maze boundaries and frames."""

import pygame


class Wall(pygame.sprite.Sprite):
    """Rectangular wall or frame sprite."""

    def __init__(
        self,
        width: int,
        height: int,
        coordinates: tuple[int, int],
        color: str = "white",
        name: str = "wall",
    ) -> None:
        """Initialize a wall sprite.

        Args:
            width: Width of the wall in pixels.
            height: Height of the wall in pixels.
            coordinates: Top-left coordinates for placement.
            color: Fill color.
            name: Sprite identifier.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        x, y = coordinates
        self.rect.x = x
        self.rect.y = y
        self.name = name
