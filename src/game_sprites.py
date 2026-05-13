"""Sprite implementations for the player and ghosts."""

from abc import ABC, abstractmethod
from enum import Enum
import random
import math
import pygame
from typing import Any, cast
from src.game import Game
from src.engine import Engine
from pygame.math import Vector2


class Direction(Enum):
    """Cardinal directions used for sprite movement."""

    WEST = 0
    SOUTH = 1
    EAST = 2
    NORTH = 3


class GameSprite(pygame.sprite.Sprite):
    """Base sprite with animation and movement helpers."""

    def __init__(
        self, game: Game, sprite_coordinates: tuple[int, int]
    ) -> None:
        """Initialize sprite animation frames and position.

        Args:
            game: Game instance providing state and collisions.
            sprite_coordinates: Sprite sheet coordinates for animations.
        """
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = pygame.image.load(
            "assets/ElementSheet.png"
        ).convert_alpha()
        self.images: list[pygame.surface.Surface] = []
        self.x, self.y = sprite_coordinates
        self.set_animation()
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.direction: Direction = Direction.EAST
        self.disered_direction: Direction = self.direction
        self.last_update = pygame.time.get_ticks()
        self.frame_cooldown = 150
        self.game = game

    def get_sprite(
        self,
        sheet: pygame.surface.Surface,
        frame: tuple[int, int],
        width: int,
        height: int,
        scale: int = 1,
    ) -> pygame.surface.Surface:
        """Extract and scale a frame from the sprite sheet.

        Args:
            sheet: Sprite sheet surface.
            frame: Frame coordinates in the sheet.
            width: Frame width in pixels.
            height: Frame height in pixels.
            scale: Scale multiplier.

        Returns:
            Scaled frame surface with padding.
        """
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

    def set_animation(self) -> None:
        """Populate the animation frames for this sprite."""
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

    def get_coordinates(self) -> tuple[int, int]:
        """Return the current maze coordinates for the sprite.

        Returns:
            Tuple of (x, y) grid coordinates.
        """
        return self.rect.x // 40, self.rect.y // 40

    def get_next_rect(self, direction: Direction, speed: int) -> pygame.Rect:
        """Compute the next rect given a direction and speed.

        Args:
            direction: Direction of movement.
            speed: Pixels to move.

        Returns:
            A rect representing the next position.
        """
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
    ) -> None:
        """Move the sprite while updating animation frames.

        Args:
            frame_index: Mapping of direction to animation frame indices.
            speed: Movement speed in pixels per update.
        """
        if not self.game.timer.paused:
            if self.direction != self.disered_direction:
                if (
                    self.get_next_rect(
                        self.disered_direction, speed
                    ).collidelist(self.game.walls.sprites())
                    == -1
                    and self.rect.x % 40 == 10
                    and self.rect.y % 40 == 10
                ):
                    self.direction = self.disered_direction
            if (
                self.get_next_rect(self.direction, speed).collidelist(
                    self.game.walls.sprites()
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
    """Player-controlled Pac-Man sprite."""

    def __init__(self, game: Game, engine: Engine) -> None:
        """Initialize the player sprite and engine reference.

        Args:
            game: Game instance for collisions and state.
            engine: Engine instance for global state and audio.
        """
        super().__init__(game, (0, 3))
        self.engine = engine
        self.last_pos = self.get_coordinates()

    def pacgum(self) -> None:
        """Handle collisions with regular pacgums."""
        pacgums = self.game.pacgums.sprites()
        index = self.rect.collidelist(pacgums)
        if index != -1:
            if self.engine.music_active:
                self.engine.music.pacgum_sound_effect()
            self.engine.score += self.game.points_per_pacgum
            pacgums[index].kill()

    def superpacgum(self) -> None:
        """Handle collisions with super pacgums."""
        pacgums = self.game.superpacgums.sprites()
        index = self.rect.collidelist(pacgums)
        if index != -1:
            if self.engine.music_active:
                self.engine.music.superpacgum_sound_effect()
            for ghost in self.game.ghosts.sprites():
                cast(Any, ghost).set_evade()
            self.engine.score += self.game.points_per_super_pacgum
            pacgums[index].kill()

    def ghosts(self) -> None:
        """Handle collisions with ghosts."""
        ghosts = self.game.ghosts.sprites()
        index = self.rect.collidelist(ghosts)
        if index != -1:
            ghost = cast(Any, ghosts[index])
            if ghost.evade:
                ghost.rect.x = round(ghost.rect.x / 5) * 5
                ghost.rect.y = round(ghost.rect.y / 5) * 5
                ghost.eaten = True
                ghost.evade = False
                ghost.set_eaten()
                self.engine.score += self.game.points_per_ghost
            else:
                if not ghost.eaten:
                    if not self.game.cheats.invisibility:
                        self.game.respawn()

    def update(self) -> None:
        """Update the player position and check interactions."""
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
    """Base class for ghost AI behaviors."""

    def __init__(
        self,
        game: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        """Initialize a ghost sprite.

        Args:
            game: Game instance for maze and player state.
            sprite_coordinates: Sprite sheet coordinates for animations.
            spawn_coordinates: Starting pixel coordinates.
        """
        super().__init__(game, sprite_coordinates)
        self.last_pos = self.get_coordinates()
        self.last_cycle = pygame.time.get_ticks()
        self.evade = False
        self.spawn = spawn_coordinates
        self.rect.x, self.rect.y = spawn_coordinates
        self.eaten = False

    def get_neighbors_coordinates(
        self, ghost_coordinates: tuple[int, int]
    ) -> list[tuple[tuple[int, int], Direction]]:
        """Return walkable neighbor coordinates from a grid cell.

        Args:
            ghost_coordinates: Current grid coordinates.

        Returns:
            List of neighbor coordinates and directions.
        """
        x, y = ghost_coordinates
        neighbors = []
        if self.game.maze.maze[y][x][0] == "0":
            neighbors.append(((x - 1, y), Direction.WEST))
        if self.game.maze.maze[y][x][2] == "0":
            neighbors.append(((x + 1, y), Direction.EAST))
        if self.game.maze.maze[y][x][1] == "0":
            neighbors.append(((x, y + 1), Direction.SOUTH))
        if self.game.maze.maze[y][x][3] == "0":
            neighbors.append(((x, y - 1), Direction.NORTH))
        return neighbors

    def set_evade(self) -> None:
        """Switch the ghost to the evade animation state."""
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

    def set_blink(self) -> None:
        """Switch the ghost to the blinking animation state."""
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

    def set_eaten(self) -> None:
        """Switch the ghost to the eaten animation state."""
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

    def get_last_pos(self) -> tuple[int, int]:
        """Return the previous grid coordinate based on direction.

        Returns:
            Previous (x, y) grid coordinate.
        """
        if Direction.SOUTH == self.direction:
            return (self.rect.x // 40, self.rect.y // 40 - 1)
        elif Direction.NORTH == self.direction:
            return (self.rect.x // 40, self.rect.y // 40 + 1)
        elif Direction.EAST == self.direction:
            return (self.rect.x // 40 - 1, self.rect.y // 40)
        else:
            return (self.rect.x // 40 + 1, self.rect.y // 40)

    def evade_movement(self) -> None:
        """Update target direction while in evade mode."""
        pos = self.get_coordinates()
        self.last_pos = self.get_last_pos()
        if self.game.maze.maze[pos[1]][pos[0]].count("0") == 1:
            self.disered_direction = Direction((self.direction.value + 2) % 4)
        if self.game.maze.maze[pos[1]][pos[0]].count("0") == 2:
            if (
                self.game.maze.maze[pos[1]][pos[0]][self.direction.value]
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
        if self.game.maze.maze[pos[1]][pos[0]].count("0") >= 3:
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
            self.disered_direction = random.choice(neighbors)[1]

    def evade_cycle(self) -> None:
        """Run the full evade cycle, including animation changes."""
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
            },
            1,
        )

    def scatter_cycle(self) -> None:
        """Handle the scatter timing behavior for ghosts."""
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

    def eaten_cycle(self) -> None:
        """Handle movement and reset when a ghost is eaten."""
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
                self.disered_direction = self.target_player(
                    self.game.player.get_coordinates()
                )
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

    def target_player(self, player_coordinates: tuple[int, int]) -> Direction:
        """Compute a direction that moves toward a target coordinate.

        Args:
            player_coordinates: Target grid coordinates.

        Returns:
            Direction to move toward the target.
        """
        self.game.maze.entry = self.get_coordinates()
        self.game.maze.exit = player_coordinates
        solution = self.game.maze.parser(self.game.maze.solve())
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
    def update(self) -> None:
        """Update the ghost state for the current frame."""
        pass


class RedGhost(Ghost):
    """Ghost that directly chases the player."""

    def __init__(
        self,
        game: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        """Initialize the red ghost.

        Args:
            game: Game instance for maze and player state.
            sprite_coordinates: Sprite sheet coordinates for animations.
            spawn_coordinates: Starting pixel coordinates.
        """
        super().__init__(game, sprite_coordinates, spawn_coordinates)
        self.last_pos = self.get_coordinates()

    def get_neighbors_coordinates(
        self, ghost_coordinates: tuple[int, int]
    ) -> list[tuple[tuple[int, int], Direction]]:
        """Return neighbor coordinates for red ghost movement.

        Args:
            ghost_coordinates: Current grid coordinates.

        Returns:
            List of neighbor coordinates and directions.
        """
        x, y = ghost_coordinates
        neighbors = []
        if self.game.maze.maze[y][x][0] == "0":
            neighbors.append(((x - 1, y), Direction.WEST))
        if self.game.maze.maze[y][x][2] == "0":
            neighbors.append(((x + 1, y), Direction.EAST))
        if self.game.maze.maze[y][x][1] == "0":
            neighbors.append(((x, y + 1), Direction.SOUTH))
        if self.game.maze.maze[y][x][3] == "0":
            neighbors.append(((x, y - 1), Direction.NORTH))
        return neighbors

    def update(self) -> None:
        """Update red ghost movement and behavior."""
        if self.evade:
            self.evade_cycle()
        elif self.eaten:
            self.eaten_cycle()
        else:
            target_coordinates = self.game.player.get_coordinates()
            if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
                self.disered_direction = self.target_player(target_coordinates)
                self.scatter_cycle()
            self.movement(
                {
                    Direction.SOUTH: (2, 3),
                    Direction.NORTH: (6, 7),
                    Direction.EAST: (0, 1),
                    Direction.WEST: (4, 5),
                },
                1,
            )


class PinkGhost(Ghost):
    """Ghost that targets a point in front of the player."""

    def __init__(
        self,
        game: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        """Initialize the pink ghost.

        Args:
            game: Game instance for maze and player state.
            sprite_coordinates: Sprite sheet coordinates for animations.
            spawn_coordinates: Starting pixel coordinates.
        """
        super().__init__(game, sprite_coordinates, spawn_coordinates)
        self.last_pos = self.get_coordinates()

    def coordinate_is_in_front_player(
        self,
        target_coordinate: Vector2,
        player_coordinate: tuple[int, int],
        i: int,
    ) -> bool:
        """Check if a coordinate is exactly i steps ahead of the player.

        Args:
            target_coordinate: Candidate coordinate to test.
            player_coordinate: Player grid coordinates.
            i: Expected path length.

        Returns:
            True if the coordinate matches the expected distance.
        """
        self.game.maze.entry = (
            int(player_coordinate[0]),
            int(player_coordinate[1]),
        )
        self.game.maze.exit = (
            int(target_coordinate[0]),
            int(target_coordinate[1]),
        )
        solution = self.game.maze.parser(self.game.maze.solve())
        if len(solution) != i:
            return False
        return True

    def is_valid_coordinate(
        self, target_coordinate: Vector2 | tuple[int, int]
    ) -> bool:
        """Validate a target coordinate inside the maze.

        Args:
            target_coordinate: Coordinate to validate.

        Returns:
            True if the coordinate is walkable within bounds.
        """
        if target_coordinate[0] < 0 or target_coordinate[0] >= self.game.width:
            return False
        if (
            target_coordinate[1] < 0
            or target_coordinate[1] >= self.game.height
        ):
            return False
        if target_coordinate in self.game.maze.forty_two_cell:
            return False

        return True

    def target(self, player_coordinates: tuple[int, int]) -> Direction:
        """Determine the desired direction based on player position.

        Args:
            player_coordinates: Player grid coordinates.

        Returns:
            Direction toward the selected target.
        """
        i = 4
        while True:
            coords = [(-i, 0), (0, i), (i, 0), (0, -i)]
            target = Vector2(player_coordinates) - Vector2(
                coords[self.game.player.direction.value]
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

        self.game.maze.entry = self.get_coordinates()
        self.game.maze.exit = (int(target[0]), int(target[1]))
        self.target_player((int(target[0]), int(target[1])))
        solution = self.game.maze.parser(self.game.maze.solve())
        if len(solution) <= 4:
            self.game.maze.exit = player_coordinates
            target = Vector2(player_coordinates)
        return self.target_player((int(target[0]), int(target[1])))

    def update(self) -> None:
        """Update pink ghost movement and behavior."""
        if self.evade:
            self.evade_cycle()
        elif self.eaten:
            self.eaten_cycle()
        else:
            if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
                target_coordinates = self.game.player.get_coordinates()
                self.disered_direction = self.target(target_coordinates)
                self.scatter_cycle()
            self.movement(
                {
                    Direction.SOUTH: (2, 3),
                    Direction.NORTH: (6, 7),
                    Direction.EAST: (0, 1),
                    Direction.WEST: (4, 5),
                },
                1,
            )


class BlueGhost(Ghost):
    """Ghost that targets a point relative to the red ghost."""

    def __init__(
        self,
        game: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        """Initialize the blue ghost.

        Args:
            game: Game instance for maze and player state.
            sprite_coordinates: Sprite sheet coordinates for animations.
            spawn_coordinates: Starting pixel coordinates.
        """
        super().__init__(game, sprite_coordinates, spawn_coordinates)
        self.last_pos = self.get_coordinates()

    def coordinate_is_in_front_player(
        self,
        target_coordinate: Vector2,
        player_coordinate: tuple[int, int],
        i: int,
    ) -> bool:
        """Check if a coordinate is exactly i steps ahead of the player.

        Args:
            target_coordinate: Candidate coordinate to test.
            player_coordinate: Player grid coordinates.
            i: Expected path length.

        Returns:
            True if the coordinate matches the expected distance.
        """
        self.game.maze.entry = (
            int(player_coordinate[0]),
            int(player_coordinate[1]),
        )
        self.game.maze.exit = (
            int(target_coordinate[0]),
            int(target_coordinate[1]),
        )
        solution = self.game.maze.parser(self.game.maze.solve())
        if len(solution) != i:
            return False
        return True

    def is_valid_coordinate(
        self, target_coordinate: Vector2 | tuple[int, int]
    ) -> bool:
        """Validate a target coordinate inside the maze.

        Args:
            target_coordinate: Coordinate to validate.

        Returns:
            True if the coordinate is walkable within bounds.
        """
        if target_coordinate[0] < 0 or target_coordinate[0] >= self.game.width:
            return False
        if (
            target_coordinate[1] < 0
            or target_coordinate[1] >= self.game.height
        ):
            return False
        if target_coordinate in self.game.maze.forty_two_cell:
            return False

        return True

    def target(self, player_coordinates: tuple[int, int]) -> Direction:
        """Determine the desired direction based on red ghost position.

        Args:
            player_coordinates: Player grid coordinates.

        Returns:
            Direction toward the selected target.
        """
        red_ghost: list[RedGhost] = [
            sprite
            for sprite in self.game.ghosts.sprites()
            if isinstance(sprite, RedGhost)
        ]
        red_position = red_ghost[0].get_coordinates()
        target: Vector2 = (
            Vector2(player_coordinates) - Vector2(red_position)
        ) * 2 + Vector2(red_position)
        while True:
            if target == Vector2(player_coordinates):
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
            target = Vector2(player_coordinates)
        self.game.maze.entry = self.get_coordinates()
        self.game.maze.exit = (int(target[0]), int(target[1]))
        return self.target_player((int(target[0]), int(target[1])))

    def update(self) -> None:
        """Update blue ghost movement and behavior."""
        if self.evade:
            self.evade_cycle()
        elif self.eaten:
            self.eaten_cycle()
        else:
            if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
                target_coordinates = self.game.player.get_coordinates()
                self.disered_direction = self.target(target_coordinates)
                self.scatter_cycle()
            self.movement(
                {
                    Direction.SOUTH: (2, 3),
                    Direction.NORTH: (6, 7),
                    Direction.EAST: (0, 1),
                    Direction.WEST: (4, 5),
                },
                1,
            )


class OrangeGhost(Ghost):
    """Ghost that alternates between chase and scatter based on distance."""

    def __init__(
        self,
        game: Game,
        sprite_coordinates: tuple[int, int],
        spawn_coordinates: tuple[int, int],
    ) -> None:
        """Initialize the orange ghost.

        Args:
            game: Game instance for maze and player state.
            sprite_coordinates: Sprite sheet coordinates for animations.
            spawn_coordinates: Starting pixel coordinates.
        """
        super().__init__(game, sprite_coordinates, spawn_coordinates)
        self.last_pos = self.get_coordinates()

    def get_neighbors_coordinates(
        self, ghost_coordinates: tuple[int, int]
    ) -> list[tuple[tuple[int, int], Direction]]:
        """Return neighbor coordinates for orange ghost movement.

        Args:
            ghost_coordinates: Current grid coordinates.

        Returns:
            List of neighbor coordinates and directions.
        """
        x, y = ghost_coordinates
        neighbors = []
        if self.game.maze.maze[y][x][0] == "0":
            neighbors.append(((x - 1, y), Direction.WEST))
        if self.game.maze.maze[y][x][2] == "0":
            neighbors.append(((x + 1, y), Direction.EAST))
        if self.game.maze.maze[y][x][1] == "0":
            neighbors.append(((x, y + 1), Direction.SOUTH))
        if self.game.maze.maze[y][x][3] == "0":
            neighbors.append(((x, y - 1), Direction.NORTH))
        return neighbors

    def target(self, player_coordinates: tuple[int, int]) -> None:
        """Update the desired direction based on player distance.

        Args:
            player_coordinates: Player grid coordinates.
        """
        pos = self.get_coordinates()
        distance = math.sqrt(
            (pos[0] - player_coordinates[0]) ** 2
            + (pos[1] - player_coordinates[1]) ** 2
        )
        self.last_pos = self.get_last_pos()
        if self.game.maze.maze[pos[1]][pos[0]].count("0") == 1:
            if pos == (self.spawn[0] // 40, self.spawn[1] // 40):
                self.disered_direction = self.target_player(player_coordinates)
            else:
                self.disered_direction = Direction(
                    (self.direction.value + 2) % 4
                )
        if self.game.maze.maze[pos[1]][pos[0]].count("0") == 2:
            if (
                self.game.maze.maze[pos[1]][pos[0]][self.direction.value]
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
        if self.game.maze.maze[pos[1]][pos[0]].count("0") >= 3:
            if distance >= 4:
                self.disered_direction = self.target_player(player_coordinates)
            else:
                self.disered_direction = self.target_player(
                    (self.spawn[0] // 40, self.spawn[1] // 40)
                )

    def update(self) -> None:
        """Update orange ghost movement and behavior."""
        if self.evade:
            self.evade_cycle()
        elif self.eaten:
            self.eaten_cycle()
        else:
            if self.rect.x % 40 == 10 and self.rect.y % 40 == 10:
                self.target(self.game.player.get_coordinates())
                self.scatter_cycle()
            self.movement(
                {
                    Direction.SOUTH: (2, 3),
                    Direction.NORTH: (6, 7),
                    Direction.EAST: (0, 1),
                    Direction.WEST: (4, 5),
                },
                1,
            )
