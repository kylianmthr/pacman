import pygame

from src.player import Player
from src.wall import Wall
from mazegen import generator


class Engine:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.running = True
        self.frame_rate = 60
        self.screen_width = width * 40 + 10
        self.screen_height = height * 40 + 40
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(Player())
        self.walls = pygame.sprite.Group()
        self.maze = generator.MazeGenerator(
            self.width,
            self.height,
            seed,
            (0, 0),
            (self.width - 1, self.height - 1),
        )
        self.maze.generate((0, 0))
        self.maze.dig()

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

    def event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                walls = self.walls.sprites()
                walls[1] = walls[1].image.fill("blue")
                self.screen.fill("black")
                self.walls.draw(self.screen)
                pygame.display.flip()

    def run(self) -> None:
        pygame.init()
        self.sprites.draw(self.screen)
        pygame.display.flip()
        while self.running:
            self.event()
            self.sprites.sprites()[0].walk()
            self.screen.fill("black")
            self.sprites.draw(self.screen)
            self.clock.tick(self.frame_rate)
        pygame.quit()
