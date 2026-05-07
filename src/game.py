import pygame
from src.pacgum import Pacgum
from src.wall import Wall
from mazegen import generator
import random


class Game:
    def __init__(self, screen, width, height, seed) -> None:
        from src.game_sprites import Player, PinkGhost, RedGhost

        self.score = 0
        self.width = width
        self.height = height
        self.screen = screen
        self.sprites = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.player = Player(self)
        self.player.rect.x = 10
        self.player.rect.y = 10
        self.maze = generator.MazeGenerator(
            self.width,
            self.height,
            seed,
            (0, 0),
            (self.width - 1, self.height - 1),
        )
        self.maze.generate((0, 0))
        self.maze.dig()
        self.red_ghost = RedGhost(self, (0, 6), (10, 10))
        self.pink_ghost = PinkGhost(self, (0, 8), (10, 10))
        self.ghosts.add(self.red_ghost)
        self.ghosts.add(self.pink_ghost)
        self.sprites.add(self.player)
        self.sprites.add(self.red_ghost)
        self.sprites.add(self.pink_ghost)
        self.walls = pygame.sprite.Group()
        self.pacgums = pygame.sprite.Group()
        self.superpacgums = pygame.sprite.Group()
        self.create_walls()
        self.create_pacgums()

    def create_walls(self) -> None:
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
        cells = [
            (row, col)
            for row in range(len(self.maze.maze))
            for col in range(len(self.maze.maze[0]))
        ]
        return random.sample(cells, 4)

    def create_pacgums(self) -> None:
        offset_y = 23
        y = 0
        superpacugums = self.get_superpacgum()
        for row in self.maze.maze:
            x = 0
            offset_x = 23
            for col in row:
                if col != "1111":
                    if (x, y) in superpacugums:
                        pacgum = Pacgum(5, (offset_x, offset_y))
                        self.superpacgums.add(pacgum)
                        self.sprites.add(pacgum)
                    else:
                        pacgum = Pacgum(2, (offset_x, offset_y))
                        self.pacgums.add(pacgum)
                        self.sprites.add(pacgum)
                x += 1
                offset_x += 40
            y += 1
            offset_y += 40

    def event(self, event) -> None:
        from src.game_sprites import Direction

        if event.type == pygame.KEYDOWN:
            player = self.sprites.sprites()[0]
            if event.key == pygame.K_LEFT:
                player.disered_direction = Direction.WEST
            if event.key == pygame.K_DOWN:
                player.disered_direction = Direction.SOUTH
            if event.key == pygame.K_UP:
                player.disered_direction = Direction.NORTH
            if event.key == pygame.K_RIGHT:
                player.disered_direction = Direction.EAST

    def update(self) -> None:
        self.sprites.update()
        self.screen.fill("black")
        self.sprites.draw(self.screen)
