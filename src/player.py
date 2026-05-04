from enum import Enum
import pygame
from src.engine import Engine
from src.game import Game


class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


class Player(pygame.sprite.Sprite):
    def __init__(self, engine: Game) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = pygame.image.load(
            "assets/ElementSheet.png"
        ).convert_alpha()
        self.images = []
        self.set_animation()
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.direction: Direction = Direction.EAST
        self.disered_direction: Direction = self.direction
        self.last_update = pygame.time.get_ticks()
        self.frame_cooldown = 150
        self.engine = engine

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
            sheet, (0, 0), (frame[0] * width, frame[1] * height, 60, 60)
        )
        image = pygame.transform.scale(image, (width * scale, height * scale))
        padding_image = pygame.Surface(
            (width + 6, height + 6), pygame.SRCALPHA
        )
        padding_image.blit(image, (3, 3))
        # padding_image = pygame.transform.scale(
        #    image, (width * scale, height * scale)
        # )
        return padding_image

    def set_animation(self):
        for i in range(8):
            self.images.append(
                self.get_sprite(self.sprite_sheet, (i, 3), 24, 24, 1)
            )

    def get_next_rect(self, direction):
        next_rect = self.rect.copy()
        next_rect.x += (
            2
            if direction == Direction.EAST
            else -2
            if direction == Direction.WEST
            else 0
        )
        next_rect.y += (
            2
            if direction == Direction.SOUTH
            else -2
            if direction == Direction.NORTH
            else 0
        )
        return next_rect

    def movement(self):
        if self.direction != self.disered_direction:
            if (
                self.get_next_rect(self.disered_direction).collidelist(
                    self.engine.walls.sprites()
                )
                == -1
                and self.rect.x % 40 == 10
                and self.rect.y % 40 == 10
            ):
                self.direction = self.disered_direction
        if (
            self.get_next_rect(self.direction).collidelist(
                self.engine.walls.sprites()
            )
            == -1
        ):
            if self.direction == Direction.SOUTH:
                self.rect.y += 2
            if self.direction == Direction.NORTH:
                self.rect.y -= 2
            if self.direction == Direction.EAST:
                self.rect.x += 2
            if self.direction == Direction.WEST:
                self.rect.x -= 2
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.frame_cooldown:
                self.last_update = current_time
                if self.direction == Direction.SOUTH:
                    self.current_frame = 5 if self.current_frame == 7 else 7
                if self.direction == Direction.NORTH:
                    self.current_frame = 1 if self.current_frame == 3 else 3
                if self.direction == Direction.EAST:
                    self.current_frame = 4 if self.current_frame == 6 else 6
                if self.direction == Direction.WEST:
                    self.current_frame = 0 if self.current_frame == 2 else 2
                self.image = self.images[self.current_frame]

    def pacgum(self):
        pacgums = self.engine.pacgums.sprites()
        index = self.rect.collidelist(pacgums)
        if index != -1:
            self.engine.score += 1
            pacgums[index].kill()

    def superpacgum(self):
        pacgums = self.engine.superpacgums.sprites()
        index = self.rect.collidelist(pacgums)
        if index != -1:
            # faire un truc
            pacgums[index].kill()

    def update(self):
        self.movement()
        self.pacgum()
        self.superpacgum()
