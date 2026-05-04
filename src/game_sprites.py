from abc import ABC, abstractmethod
from enum import Enum
import re
import pygame
from src.game import Game
import math


class Direction(Enum):
    WEST = 0
    SOUTH = 1
    EAST = 2
    NORTH = 3


class GameSprite(pygame.sprite.Sprite):
    def __init__(
        self, engine: Game, sprite_coordinates: tuple[int, int]
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = pygame.image.load(
            "assets/ElementSheet.png"
        ).convert_alpha()
        self.images = []
        self.x, self.y = sprite_coordinates
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
        return padding_image

    def set_animation(self):
        for i in range(8):
            self.images.append(
                self.get_sprite(
                    self.sprite_sheet,
                    (
                        self.x + i,
                        self.y,
                    ),
                    24,
                    24,
                    1,
                )
            )

    def get_coordinates(self):
        return self.rect.x // 40, self.rect.y // 40

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


class Player(GameSprite):
    def __init__(self, engine: Game) -> None:
        super().__init__(engine, (0, 3))

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


class Ghost(ABC, GameSprite):
    def __init__(
        self, engine: Game, sprite_coordinates: tuple[int, int]
    ) -> None:
        super().__init__(engine, sprite_coordinates)
        self.last_pos = self.get_coordinates()

    def get_neighbors_coordinates(self, ghost_coordinates: tuple[int, int]):
        x, y = ghost_coordinates
        neighbors = []
        # The walls bits are in LSB order: WEST, SOUTH, EAST, NORTH
        if self.engine.maze.maze[y][x][0] == "0":
            neighbors.append(((x - 1, y), Direction.WEST))
        if self.engine.maze.maze[y][x][2] == "0":
            neighbors.append(((x + 1, y), Direction.EAST))
        if self.engine.maze.maze[y][x][1] == "0":
            neighbors.append(((x, y + 1), Direction.SOUTH))
        if self.engine.maze.maze[y][x][3] == "0":
            neighbors.append(((x, y - 1), Direction.NORTH))
        return neighbors

    def target_player(self, player_coordinates: tuple[int, int]):
        self.engine.maze.entry = self.get_coordinates()
        self.engine.maze.exit = player_coordinates
        solution = self.engine.maze.parser(self.engine.maze.solve())
        if solution:
            if solution[0] == "N":
                return Direction.NORTH
            elif solution[0] == "S":
                return Direction.SOUTH
            elif solution[0] == "E":
                return Direction.EAST
            else:
                return Direction.WEST
        return Direction.WEST

    def update(self):
        target_coordinates = self.engine.player.get_coordinates()
        if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
            print("test")
            self.disered_direction = self.target_player(target_coordinates)
        self.movement()
