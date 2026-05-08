from abc import ABC, abstractmethod
from enum import Enum
import random
import math
import pygame
from src.game import Game
from pygame.math import Vector2


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

    def get_next_rect(self, direction, speed):
        next_rect = self.rect.copy()
        next_rect.x += (
            speed
            if direction == Direction.EAST
            else -speed
            if direction == Direction.WEST
            else 0
        )
        next_rect.y += (
            speed
            if direction == Direction.SOUTH
            else -speed
            if direction == Direction.NORTH
            else 0
        )
        return next_rect

    def movement(
        self, frame_index: dict[Direction, tuple[int, int]], speed: int = 2
    ):
        if self.direction != self.disered_direction:
            if (
                self.get_next_rect(self.disered_direction, speed).collidelist(
                    self.engine.walls.sprites()
                )
                == -1
                and self.rect.x % 40 == 10
                and self.rect.y % 40 == 10
            ):
                self.direction = self.disered_direction
        if (
            self.get_next_rect(self.direction, speed).collidelist(
                self.engine.walls.sprites()
            )
            == -1
        ):
            if self.direction == Direction.SOUTH:
                self.rect.y += speed
            if self.direction == Direction.NORTH:
                self.rect.y -= speed
            if self.direction == Direction.EAST:
                self.rect.x += speed
            if self.direction == Direction.WEST:
                self.rect.x -= speed
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.frame_cooldown:
                self.last_update = current_time
                for direction, frames in frame_index.items():
                    if self.direction == direction:
                        self.current_frame = (
                            frames[0]
                            if self.current_frame == frames[1]
                            else frames[1]
                        )
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
            for ghost in self.engine.ghosts.sprites():
                ghost.set_evade()
            pacgums[index].kill()

    def ghosts(self):
        ghosts = self.engine.ghosts.sprites()
        index = self.rect.collidelist(ghosts)
        if index != -1:
            ghost = ghosts[index]
            if ghost.evade:
                ghost.rect.x = round(ghost.rect.x / 5) * 5
                ghost.rect.y = round(ghost.rect.y / 5) * 5
                ghost.eaten = True
                ghost.evade = False
                ghost.set_eaten()
            else:
                pass
                # le game over

    def update(self):
        self.movement(
            {
                Direction.SOUTH: (5, 7),
                Direction.NORTH: (1, 3),
                Direction.EAST: (4, 6),
                Direction.WEST: (0, 2),
            }
        )
        self.pacgum()
        self.superpacgum()
        self.ghosts()


class Ghost(ABC, GameSprite):
    def __init__(
        self,
        engine: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        super().__init__(engine, sprite_coordinates)
        self.last_pos = self.get_coordinates()
        self.last_cycle = pygame.time.get_ticks()
        self.evade = False
        self.spawn = spawn_coordinates
        self.rect.x, self.rect.y = spawn_coordinates
        self.eaten = False

    def get_neighbors_coordinates(self, ghost_coordinates: tuple[int, int]):
        x, y = ghost_coordinates
        neighbors = []
        if self.engine.maze.maze[y][x][0] == "0":
            neighbors.append(((x - 1, y), Direction.WEST))
        if self.engine.maze.maze[y][x][2] == "0":
            neighbors.append(((x + 1, y), Direction.EAST))
        if self.engine.maze.maze[y][x][1] == "0":
            neighbors.append(((x, y + 1), Direction.SOUTH))
        if self.engine.maze.maze[y][x][3] == "0":
            neighbors.append(((x, y - 1), Direction.NORTH))
        return neighbors

    def set_evade(self):
        self.evade = True
        self.last_cycle = pygame.time.get_ticks()
        self.images = []
        for i in range(2):
            self.images.append(
                self.get_sprite(
                    self.sprite_sheet,
                    (
                        8 + i,
                        4,
                    ),
                    24,
                    24,
                    1,
                )
            )

    def set_blink(self):
        self.images = []
        for i in range(2):
            self.images.append(
                self.get_sprite(
                    self.sprite_sheet,
                    (
                        7 + i,
                        4,
                    ),
                    24,
                    24,
                    1,
                )
            )

    def set_eaten(self):
        self.images = []
        for i in range(8):
            self.images.append(
                self.get_sprite(
                    self.sprite_sheet,
                    (
                        8 + i,
                        9,
                    ),
                    24,
                    24,
                    1,
                )
            )

    def get_last_pos(self):
        if Direction.SOUTH == self.direction:
            return (self.rect.x // 40, self.rect.y // 40 - 1)
        elif Direction.NORTH == self.direction:
            return (self.rect.x // 40, self.rect.y // 40 + 1)
        elif Direction.EAST == self.direction:
            return (self.rect.x // 40 - 1, self.rect.y // 40)
        else:
            return (self.rect.x // 40 + 1, self.rect.y // 40)

    def evade_movement(self):
        pos = self.get_coordinates()
        self.last_pos = self.get_last_pos()
        if self.engine.maze.maze[pos[1]][pos[0]].count("0") == 1:
            self.disered_direction = Direction((self.direction.value + 2) % 4)
        if self.engine.maze.maze[pos[1]][pos[0]].count("0") == 2:
            if (
                self.engine.maze.maze[pos[1]][pos[0]][self.direction.value]
                == "1"
            ):
                neighbors = self.get_neighbors_coordinates(pos)
                if (
                    self.last_pos,
                    Direction((self.direction.value + 2) % 4),
                ) in neighbors:
                    neighbors.remove(
                        (
                            self.last_pos,
                            Direction((self.direction.value + 2) % 4),
                        )
                    )
                print(neighbors)
                print(self.last_pos)
                self.disered_direction = neighbors[0][1]
        if self.engine.maze.maze[pos[1]][pos[0]].count("0") >= 3:
            neighbors = self.get_neighbors_coordinates(pos)
            if (
                self.last_pos,
                Direction((self.direction.value + 2) % 4),
            ) in neighbors:
                neighbors.remove(
                    (
                        self.last_pos,
                        Direction((self.direction.value + 2) % 4),
                    )
                )
                print(self.last_pos)
            self.disered_direction = random.choice(neighbors)[1]

    def evade_cycle(self):
        current_time = pygame.time.get_ticks()
        if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
            self.evade_movement()
        if current_time - self.last_cycle >= 10000:
            self.evade = False
            self.last_cycle = current_time
            self.images = []
            self.set_animation()
        if 7000 <= current_time - self.last_cycle >= 8000:
            self.images = []
            self.set_blink()
        self.movement(
            {
                Direction.SOUTH: (0, 1),
                Direction.NORTH: (0, 1),
                Direction.EAST: (0, 1),
                Direction.WEST: (0, 1),
            }
        )

    def scatter_cycle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_cycle >= 10000:
            self.disered_direction = self.target_player(
                (self.spawn[0] // 40, self.spawn[1] // 40)
            )
        if self.get_coordinates() == (
            self.spawn[0] // 40,
            self.spawn[1] // 40,
        ):
            self.last_cycle = current_time
        if current_time - self.last_cycle >= 15000:
            self.last_cycle = current_time

    def eaten_cycle(self):
        current_time = pygame.time.get_ticks()
        if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
            if self.get_coordinates() == (
                self.spawn[0] // 40,
                self.spawn[1] // 40,
            ):
                self.last_cycle = current_time
                self.images = []
                self.set_animation()
                self.eaten = False
        if self.eaten:
            if (
                float(self.get_coordinates()[0]),
                float(self.get_coordinates()[1]),
            ) != (
                self.spawn[0] / 40,
                self.spawn[1] / 40,
            ):
                self.disered_direction = self.target_player(
                    (
                        self.spawn[0] // 40,
                        self.spawn[1] // 40,
                    )
                )
                self.movement(
                    {
                        Direction.SOUTH: (2, 3),
                        Direction.NORTH: (6, 7),
                        Direction.EAST: (0, 1),
                        Direction.WEST: (4, 5),
                    },
                    5,
                )

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

    @abstractmethod
    def update(self):
        pass


class RedGhost(Ghost):
    def __init__(
        self,
        engine: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        super().__init__(engine, sprite_coordinates, spawn_coordinates)
        self.last_pos = self.get_coordinates()

    def get_neighbors_coordinates(self, ghost_coordinates: tuple[int, int]):
        x, y = ghost_coordinates
        neighbors = []
        if self.engine.maze.maze[y][x][0] == "0":
            neighbors.append(((x - 1, y), Direction.WEST))
        if self.engine.maze.maze[y][x][2] == "0":
            neighbors.append(((x + 1, y), Direction.EAST))
        if self.engine.maze.maze[y][x][1] == "0":
            neighbors.append(((x, y + 1), Direction.SOUTH))
        if self.engine.maze.maze[y][x][3] == "0":
            neighbors.append(((x, y - 1), Direction.NORTH))
        return neighbors

    def update(self):
        if self.evade:
            self.evade_cycle()
        elif self.eaten:
            self.eaten_cycle()
        else:
            target_coordinates = self.engine.player.get_coordinates()
            if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
                self.disered_direction = self.target_player(target_coordinates)
                self.scatter_cycle()
            self.movement(
                {
                    Direction.SOUTH: (2, 3),
                    Direction.NORTH: (6, 7),
                    Direction.EAST: (0, 1),
                    Direction.WEST: (4, 5),
                }
            )


class PinkGhost(Ghost):
    def __init__(
        self,
        engine: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        super().__init__(engine, sprite_coordinates, spawn_coordinates)
        self.last_pos = self.get_coordinates()

    def coordinate_is_in_front_player(
        self, target_coordinate, player_coordinate, i
    ):
        self.engine.maze.entry = (
            int(player_coordinate[0]),
            int(player_coordinate[1]),
        )
        self.engine.maze.exit = (
            int(target_coordinate[0]),
            int(target_coordinate[1]),
        )
        solution = self.engine.maze.parser(self.engine.maze.solve())
        if len(solution) != i:
            return False
        return True

    def is_valid_coordinate(self, target_coordinate):
        if (
            target_coordinate[0] < 0
            or target_coordinate[0] >= self.engine.width
        ):
            return False
        if (
            target_coordinate[1] < 0
            or target_coordinate[1] >= self.engine.height
        ):
            return False
        if target_coordinate in self.engine.maze.forty_two_cell:
            return False

        return True

    def target(self, player_coordinates: tuple[int, int]):
        i = 4
        while True:
            coords = [(-i, 0), (0, i), (i, 0), (0, -i)]
            target = Vector2(player_coordinates) - Vector2(
                coords[self.engine.player.direction.value]
            )
            if i == 0:
                break
            if not self.is_valid_coordinate(
                target,
            ):
                i -= 1
                continue
            if not self.coordinate_is_in_front_player(
                target, player_coordinates, i
            ):
                i -= 1
            else:
                break

        self.engine.maze.entry = self.get_coordinates()
        self.engine.maze.exit = (int(target[0]), int(target[1]))
        self.target_player((int(target[0]), int(target[1])))
        solution = self.engine.maze.parser(self.engine.maze.solve())
        if len(solution) <= 4:
            self.engine.maze.exit = tuple(player_coordinates)
            target = player_coordinates
        return self.target_player((int(target[0]), int(target[1])))

    def update(self):
        if self.evade:
            self.evade_cycle()
        elif self.eaten:
            self.eaten_cycle()
        else:
            if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
                target_coordinates = self.engine.player.get_coordinates()
                self.disered_direction = self.target(target_coordinates)
                self.scatter_cycle()
            self.movement(
                {
                    Direction.SOUTH: (2, 3),
                    Direction.NORTH: (6, 7),
                    Direction.EAST: (0, 1),
                    Direction.WEST: (4, 5),
                }
            )


class BlueGhost(Ghost):
    def __init__(
        self,
        engine: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        super().__init__(engine, sprite_coordinates, spawn_coordinates)
        self.last_pos = self.get_coordinates()

    def coordinate_is_in_front_player(
        self, target_coordinate, player_coordinate, i
    ):
        self.engine.maze.entry = (
            int(player_coordinate[0]),
            int(player_coordinate[1]),
        )
        self.engine.maze.exit = (
            int(target_coordinate[0]),
            int(target_coordinate[1]),
        )
        solution = self.engine.maze.parser(self.engine.maze.solve())
        if len(solution) != i:
            return False
        return True

    def is_valid_coordinate(self, target_coordinate):
        if (
            target_coordinate[0] < 0
            or target_coordinate[0] >= self.engine.width
        ):
            return False
        if (
            target_coordinate[1] < 0
            or target_coordinate[1] >= self.engine.height
        ):
            return False
        if target_coordinate in self.engine.maze.forty_two_cell:
            return False

        return True

    def target(self, player_coordinates: tuple[int, int]):
        red_position = self.engine.red_ghost.get_coordinates()
        target = red_position
        target = (
            Vector2(player_coordinates) - Vector2(red_position)
        ) * 2 + Vector2(red_position)
        while True:
            if target == player_coordinates:
                break
            if (
                not self.is_valid_coordinate(
                    target,
                )
                and target[1] > 0
                and target[0] > 0
            ):
                target -= Vector2(1, 1)
                continue
            break
        if not self.is_valid_coordinate(
            target,
        ):
            target = player_coordinates
        self.engine.maze.entry = self.get_coordinates()
        self.engine.maze.exit = (int(target[0]), int(target[1]))
        return self.target_player((int(target[0]), int(target[1])))

    def update(self):
        if self.evade:
            self.evade_cycle()
        elif self.eaten:
            self.eaten_cycle()
        else:
            if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
                target_coordinates = self.engine.player.get_coordinates()
                self.disered_direction = self.target(target_coordinates)
                self.scatter_cycle()
            self.movement(
                {
                    Direction.SOUTH: (2, 3),
                    Direction.NORTH: (6, 7),
                    Direction.EAST: (0, 1),
                    Direction.WEST: (4, 5),
                }
            )


class OrangeGhost(Ghost):
    def __init__(
        self,
        engine: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        super().__init__(engine, sprite_coordinates, spawn_coordinates)
        self.last_pos = self.get_coordinates()

    def get_neighbors_coordinates(self, ghost_coordinates: tuple[int, int]):
        x, y = ghost_coordinates
        neighbors = []
        if self.engine.maze.maze[y][x][0] == "0":
            neighbors.append(((x - 1, y), Direction.WEST))
        if self.engine.maze.maze[y][x][2] == "0":
            neighbors.append(((x + 1, y), Direction.EAST))
        if self.engine.maze.maze[y][x][1] == "0":
            neighbors.append(((x, y + 1), Direction.SOUTH))
        if self.engine.maze.maze[y][x][3] == "0":
            neighbors.append(((x, y - 1), Direction.NORTH))
        return neighbors

    def target(self, player_coordinates: tuple[int, int]):
        pos = self.get_coordinates()
        distance = math.sqrt(
            (pos[0] - player_coordinates[0]) ** 2
            + (pos[1] - player_coordinates[1]) ** 2
        )
        self.last_pos = self.get_last_pos()
        if self.engine.maze.maze[pos[1]][pos[0]].count("0") == 1:
            self.disered_direction = Direction((self.direction.value + 2) % 4)
        if self.engine.maze.maze[pos[1]][pos[0]].count("0") == 2:
            if (
                self.engine.maze.maze[pos[1]][pos[0]][self.direction.value]
                == "1"
            ):
                neighbors = self.get_neighbors_coordinates(pos)
                if (
                    self.last_pos,
                    Direction((self.direction.value + 2) % 4),
                ) in neighbors:
                    neighbors.remove(
                        (
                            self.last_pos,
                            Direction((self.direction.value + 2) % 4),
                        )
                    )
                self.disered_direction = neighbors[0][1]
        if self.engine.maze.maze[pos[1]][pos[0]].count("0") >= 3:
            if distance >= 4:
                self.disered_direction = self.target_player(player_coordinates)
            else:
                self.disered_direction = self.target_player(
                    (self.spawn[0] // 40, self.spawn[1] // 40)
                )

    def update(self):
        if self.evade:
            self.evade_cycle()
        elif self.eaten:
            self.eaten_cycle()
        else:
            if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
                self.target(self.engine.player.get_coordinates())
                self.scatter_cycle()
            self.movement(
                {
                    Direction.SOUTH: (2, 3),
                    Direction.NORTH: (6, 7),
                    Direction.EAST: (0, 1),
                    Direction.WEST: (4, 5),
                }
            )
