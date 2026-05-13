import pygame
from pygame.surface import Surface


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        name: str,
        object: pygame.font.Font | str,
        coordinates: tuple[int, int],
        position: int,
        color: str,
        scale_width: int = 40,
        scale_height: int = 40,
    ) -> None:
        super().__init__()
        self.name = name
        self.object = object
        self.position = position
        self.coordinates = coordinates
        self.color = color
        self.scale_width = scale_width
        self.scale_height = scale_height
        self.image: Surface = self.choose_type()
        self.rect = self.image.get_rect(center=coordinates)

    def choose_type(self) -> Surface:
        if isinstance(self.object, pygame.font.Font):
            return self.object.render(self.name, True, self.color, None)
        image = pygame.image.load(self.object)
        return pygame.transform.smoothscale(
            image, (self.scale_width, self.scale_height)
        )


class Text(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        color: str,
        font: pygame.font.Font,
        coordinates: tuple[int, int],
    ):
        super().__init__()
        self.coordinates = coordinates
        self.name = text
        self.color = color
        self.font = font
        self.text = text
        self.image = self.font.render(self.text, True, color, None)
        self.rect = self.image.get_rect(center=coordinates)


class TextFromRight(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        color: str,
        font: pygame.font.Font,
        coordinates: tuple[int, int],
    ):
        super().__init__()
        self.name = text
        self.color = color
        self.font = font
        self.image = self.font.render(text, True, color, None)
        self.rect = self.image.get_rect(midright=coordinates)


class TextFromLeft(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        color: str,
        font: pygame.font.Font,
        coordinates: tuple[int, int],
    ):
        super().__init__()
        self.name = text
        self.text = text
        self.color = color
        self.font = font
        self.image = self.font.render(self.text, True, color, None)
        self.rect = self.image.get_rect(midleft=coordinates)

    def get_size(self) -> tuple[int, int]:
        return self.font.size(self.text)


class Picture(pygame.sprite.Sprite):
    def __init__(
        self,
        name: str,
        path: str,
        scale_width: int,
        scale_height: int,
        coordinates: tuple[int, int],
    ):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(
            self.image, (scale_width, scale_height)
        )
        self.rect = self.image.get_rect(center=coordinates)


class Box(pygame.sprite.Sprite):
    def __init__(
        self,
        width: int,
        height: int,
        coordinates: tuple[int, int],
        alpha: int = 100,
        color: str = "black",
        name: str = "box",
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect(center=coordinates)
        self.name = name
