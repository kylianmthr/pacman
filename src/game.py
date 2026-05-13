"""Main gameplay state and update loop for a single level."""

import pygame
from src.cheat import Cheats
from src.pacgum import Pacgum
from src.wall import Wall
from mazegen import generator
from pygame import mixer
import random
from typing import Any, cast


class Game:
    """Manage the maze, sprites, and gameplay logic for a level."""

    def __init__(
        self,
        engine: Any,
        screen: pygame.surface.Surface,
        width: int,
        height: int,
        seed: int,
        points_per_pacgum: int,
        points_per_super_pacgum: int,
        points_per_ghost: int,
        lives: int,
        level_max_time: int,
        pacgum: int,
    ) -> None:
        """Initialize level state, sprites, and scoring.

        Args:
            engine: Owning engine instance.
            screen: Pygame surface used for rendering.
            width: Maze width in cells.
            height: Maze height in cells.
            seed: Random seed for the first level.
            points_per_pacgum: Score for a regular pacgum.
            points_per_super_pacgum: Score for a super pacgum.
            points_per_ghost: Score for eating a ghost.
            lives: Starting lives for the player.
            level_max_time: Level duration in seconds.
            pacgum: Number of pacgums to spawn.
        """
        from src.game_sprites import (
            Player,
            PinkGhost,
            RedGhost,
            BlueGhost,
            OrangeGhost,
            Ghost,
        )
        from src.hud import HUD
        from src.pause import PauseMenu
        from src.timer import Timer

        self.engine = engine
        self.lives = lives
        self.pause_menu = PauseMenu(self.engine)
        self.timer = Timer(level_max_time)
        self.hud = HUD(self, self.engine)
        self.width = width
        self.height = height
        self.screen = screen
        self.sprites: Any = pygame.sprite.Group()
        self.ghosts: Any = pygame.sprite.Group()
        self.player = Player(self, self.engine)
        self.player.rect.x = (self.width - 1) // 2 * 40 + 10
        self.player.rect.y = (self.height - 1) // 2 * 40 + 10
        self.maze = generator.MazeGenerator(
            self.width,
            self.height,
            seed if self.engine.level == 0 else random.randint(0, 999999),
            (0, 0),
            (self.width - 1, self.height - 1),
        )
        self.maze.generate((0, 0))
        self.maze.dig()
        ghosts: list[Ghost] = [
            RedGhost(self, (0, 6), (10, 10)),
            PinkGhost(self, (0, 8), ((self.width - 1) * 40 + 10, 10)),
            BlueGhost(
                self,
                (8, 8),
                ((self.width - 1) * 40 + 10, (self.height - 1) * 40 + 10),
            ),
            OrangeGhost(self, (0, 9), (10, (self.height - 1) * 40 + 10)),
        ]
        self.sprites.add(self.player)
        self.walls: Any = pygame.sprite.Group()
        self.pacgums: Any = pygame.sprite.Group()
        self.pacgum = pacgum
        self.superpacgums: Any = pygame.sprite.Group()
        self.create_walls()
        self.create_pacgums()
        for ghost in ghosts:
            self.ghosts.add(ghost)
            self.sprites.add(ghost)
        self.sprites.add(self.hud.score)
        self.sprites.add(self.hud.lives)
        self.sprites.add(self.hud.timer)
        self.sprites.add(self.hud.level)
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost
        self.cheats = Cheats(self)

    def create_walls(self) -> None:
        """Build wall sprites based on the generated maze."""
        offset_y = 0
        for row in self.maze.maze:
            offset_x = 0
            for col in row:
                walls = []
                if int(col[3]):
                    walls += [Wall(50, 10, (0 + offset_x, 0 + offset_y))]
                if int(col[0]):
                    walls += [Wall(10, 50, (0 + offset_x, 0 + offset_y))]
                if col == "1111":
                    walls += [
                        Wall(30, 30, (10 + offset_x, 10 + offset_y), "blue")
                    ]
                self.walls.add(walls)
                self.sprites.add(walls)
                offset_x += 40
            offset_y += 40
        bottom_wall = Wall(40 * self.width + 10, 10, (0, offset_y))
        self.walls.add(bottom_wall)
        self.sprites.add(bottom_wall)
        right_wall = Wall(10, 40 * self.height + 10, (40 * self.width, 0))
        self.walls.add(right_wall)
        self.sprites.add(right_wall)

    def get_superpacgum(self) -> list[tuple[int, int]]:
        """Return the corner coordinates for super pacgums."""
        return [
            (0, 0),
            (self.width - 1, 0),
            (self.width - 1, self.height - 1),
            (0, self.height - 1),
        ]

    def create_pacgums(self) -> None:
        """Populate the maze with pacgum and super pacgum sprites."""
        offset_y = 23
        y = 0
        superpacgums = self.get_superpacgum()
        cells = [
            (row, col)
            for row in range(len(self.maze.maze))
            for col in range(len(self.maze.maze[0]))
        ]
        for cell in superpacgums:
            if cell in cells:
                cells.remove(cell)
        for cell in self.maze.forty_two_cell:
            if cell in cells:
                cells.remove(cell)
        if self.pacgum >= self.width * self.height:
            self.pacgum = (
                self.width * self.height
                - len(superpacgums)
                - len(self.maze.forty_two_cell)
            )
        cells = random.sample(cells, self.pacgum)

        for row in self.maze.maze:
            x = 0
            offset_x = 23
            for col in row:
                if col != "1111":
                    if (x, y) in superpacgums:
                        pacgum = Pacgum(5, (offset_x, offset_y))
                        self.superpacgums.add(pacgum)
                        self.sprites.add(pacgum)
                    elif self.pacgum == 0 or (x, y) in cells:
                        pacgum = Pacgum(2, (offset_x, offset_y))
                        self.pacgums.add(pacgum)
                        self.sprites.add(pacgum)
                x += 1
                offset_x += 40
            y += 1
            offset_y += 40

    def respawn(self) -> None:
        """Respawn the player and reset ghost positions after a hit."""
        self.lives -= 1
        self.player.rect.x = (self.width - 1) // 2 * 40 + 10
        self.player.rect.y = (self.height - 1) // 2 * 40 + 10
        coords = [
            (10, 10),
            ((self.width - 1) * 40 + 10, 10),
            ((self.width - 1) * 40 + 10, (self.height - 1) * 40 + 10),
            (10, (self.height - 1) * 40 + 10),
        ]
        for i in range(len(self.ghosts.sprites())):
            current_time = pygame.time.get_ticks()
            ghost = cast(Any, self.ghosts.sprites()[i])
            ghost.rect.x = coords[i][0]
            ghost.rect.y = coords[i][1]
            ghost.eaten = False
            ghost.evade = False
            ghost.last_cycle = current_time
            ghost.images = []
            ghost.set_animation()
            ghost.direction = ghost.target_player(
                cast(Any, self.player).get_coordinates()
            )

    def event(self, event: pygame.event.Event) -> None:
        """Handle gameplay events such as movement and pause."""
        from src.game_sprites import Direction

        self.cheats.event(event)

        if event.type == pygame.KEYDOWN:
            player = cast(Any, self.sprites.sprites()[0])
            if event.key == pygame.K_LEFT:
                player.disered_direction = Direction.WEST
            if event.key == pygame.K_DOWN:
                player.disered_direction = Direction.SOUTH
            if event.key == pygame.K_UP:
                player.disered_direction = Direction.NORTH
            if event.key == pygame.K_RIGHT:
                player.disered_direction = Direction.EAST
            if event.key == pygame.K_ESCAPE:
                self.timer.toggle_pause()
            if self.timer.paused:
                if event.key == pygame.K_RETURN:
                    self.engine.running = False

    def update(self) -> None:
        """Update all sprites, draw the frame, and check level state."""
        self.sprites.update()
        self.screen.fill("black")
        self.sprites.draw(self.screen)
        if len(self.pacgums.sprites()) == 0 and not self.engine.loading:
            self.engine.loading = True
            self.engine.next_level()
        if self.lives <= 0 or self.timer.is_expired():
            self.engine.menu_active = True
            self.engine.menu.switch_menu("game_over_menu")
            mixer.music.stop()
        if self.timer.paused:
            self.pause_menu.draw()
