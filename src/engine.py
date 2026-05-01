import pygame

from src.welcome_menu import WelcomeMenu
from src.game import Game

# from src.pacgum import Pacgum
from src.wall import Wall
from mazegen import generator


class Engine:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.menu = True
        self.running = True
        self.frame_rate = 60
        self.screen_width = width * 40 + 10
        self.screen_height = height * 40 + 40
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.clock = pygame.time.Clock()
        self.welcome_menu = WelcomeMenu(
            self.screen, self.screen_width, self.screen_height
        )
        self.game = Game(self.screen, width, height, seed)

    def event(self) -> None:
        from src.player import Direction

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.menu:
                    self.menu = self.welcome_menu.event(event)
                else:
                    self.game.event(event)
            if event.type == pygame.QUIT:
                self.running = False

    def run(self) -> None:
        pygame.init()

        while self.running:
            if self.menu:
                self.welcome_menu.show_home_menu(
                    self.screen_width, self.screen_height
                )
            else:
                self.game.update()
            self.event()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        pygame.quit()
