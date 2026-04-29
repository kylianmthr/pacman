from enum import Enum
import pygame


class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = pygame.image.load(
            "assets/ElementSheet.png"
        ).convert_alpha()
        self.images = []
        self.set_animation()
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.direction: Direction = Direction.SOUTH

    def get_sprite(
        self,
        sheet,
        frame: tuple[int, int],
        width: int,
        height: int,
        scale: int = 1,
    ):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(
            sheet, (0, 0), (frame[0] * width, frame[1] * height, width, height)
        )
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image

    def set_animation(self):
        for i in range(8):
            self.images.append(
                self.get_sprite(self.sprite_sheet, (i, 3), 24, 24, 1)
            )

    def walk(self):
        if self.direction == Direction.SOUTH:
            self.rect.y += 2
            self.current_frame = 5 if self.current_frame == 7 else 7
