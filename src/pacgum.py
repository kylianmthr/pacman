import pygame


class Pacgum(pygame.sprite.Sprite):
    def __init__(self, radius: int, coordinates: tuple[int, int]) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(self.image, "yellow", (radius, radius), radius)
        self.rect = self.image.get_rect(center=coordinates)
        x, y = coordinates
        self.rect.x = x
        self.rect.y = y
        self.radius = radius
