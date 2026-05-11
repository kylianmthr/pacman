import pygame
import os

from src.models import Config
from src.menu import Menu
from src.game import Game
from src.leaderboard import Leaderboard
from src.music import Music


class Engine:
    def __init__(self, config: Config) -> None:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.color = "white"
        self.config = config
        self.menu_active = True
        self.level = 0
        self.loading = False
        self.levels = config.level
        self.seed = config.seed
        self.running = True
        self.music_active = True
        self.score = 0
        self.frame_rate = 60
        self.screen_width = self.levels[self.level].width * 40 + 10
        self.screen_height = self.levels[self.level].height * 40 + 40
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.clock = pygame.time.Clock()
        self.leaderboard = Leaderboard()
        self.menu = Menu(
            self,
        )
        self.game = Game(
            self,
            self.screen,
            self.levels[self.level].width,
            self.levels[self.level].height,
            config.seed,
            config.points_per_pacgum,
            config.points_per_super_pacgum,
            config.points_per_ghost,
        )
        self.music = Music(
            "./assets/pacman_beginning.mp3",
            "./assets/eat_dot.wav",
            "./assets/ghost.wav",
            "./assets/pacgum.wav",
        )
        self.music.start_music()

    def change_wall_color(self):
        for wall in self.game.walls:
            wall.color = self.color
            wall.image.fill(self.color)

    def next_level(self) -> None:
        self.level += 1
        self.screen_width = self.levels[self.level].width * 40 + 10
        self.screen_height = self.levels[self.level].height * 40 + 40
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.game = Game(
            self,
            self.screen,
            self.levels[self.level].width,
            self.levels[self.level].height,
            self.seed,
            self.config.points_per_pacgum,
            self.config.points_per_super_pacgum,
            self.config.points_per_ghost,
        )
        self.loading = False

    def event(self) -> None:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.menu_active:
                    self.menu.event(event)
                else:
                    self.game.event(event)
            if event.type == pygame.QUIT:
                self.running = False

    def run(self) -> None:
        pygame.init()

        while self.running:
            if self.menu_active:
                self.menu.show()
            else:
                self.game.update()
            self.event()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        pygame.quit()
