import pygame
from pygame import mixer
import os

from src.models import LevelType
from src.menu import Menu
from src.game import Game
from src.leaderboard import Leaderboard
from src.music import Music


class Engine:
    def __init__(self, levels: list[LevelType], seed: int) -> None:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.menu_active = True
        self.level = 0
        self.loading = False
        self.levels = levels
        self.seed = seed
        self.running = True
        self.music_active = True

        self.frame_rate = 60
        self.screen_width = levels[self.level].width * 40 + 10
        self.screen_height = levels[self.level].height * 40 + 40
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.clock = pygame.time.Clock()
        self.leaderboard = Leaderboard()
        self.menu = Menu(
            self.screen,
            self.screen_width,
            self.screen_height,
            self.leaderboard,
        )
        self.game = Game(
            self,
            self.screen,
            self.levels[self.level].width,
            self.levels[self.level].height,
            seed,
        )
        self.music = Music(
            "./assets/pacman_beginning.mp3",
            "./assets/eat_dot.wav",
            "./assets/ghost.wav",
            "./assets/pacgum.wav",
        )
        self.music.start_music()

    def change_wall_color(self, color):
        for wall in self.game.walls:
            wall.color = color
            wall.image.fill(color)

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
        )
        self.loading = False

    def event(self) -> None:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.menu_active:
                    menu_event = self.menu.event(event)
                    if menu_event == "start":
                        self.menu_active = False
                        if self.music_active:
                            self.music.ghost_sound_effect()
                    elif menu_event == "exit":
                        self.running = False
                    elif menu_event == "music_on":
                        self.music_active = True
                        self.music.start_music()
                    elif menu_event == "music_off":
                        self.music_active = False
                        mixer.music.stop()
                    elif menu_event == "":
                        pass
                    else:
                        self.change_wall_color(menu_event)
                        print(f"new color wall = {menu_event}")
                else:
                    self.game.event(event)
            if event.type == pygame.QUIT:
                self.running = False

    def run(self) -> None:
        pygame.init()

        while self.running:
            if self.menu_active:
                self.menu.show(self.screen_width, self.screen_height)
            else:
                self.game.update()
            self.event()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        pygame.quit()
