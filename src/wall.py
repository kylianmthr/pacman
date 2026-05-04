import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(
        self,
        width: int,
        height: int,
        coordinates: tuple[int, int],
        color: str = "white",
        name="wall",
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        x, y = coordinates
        self.rect.x = x
        self.rect.y = y
        self.name = name
