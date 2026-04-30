import pygame

from src.welcome_menu import WelcomeMenu
from src.game import Game 
from src.pacgum import Pacgum
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
        self.game = Game(self.screen, width , height, seed)

    # def event(self) -> None:
        # from src.player import Direction
        # events = pygame.event.get()
        # for event in events:
            # if event.type == pygame.QUIT:
                # self.running = False
        # self.welcome_menu.event(events)

    def event(self) -> None:
        from src.player import Direction
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.menu = False
                if self.menu:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.welcome_menu.item_selection(-1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.welcome_menu.item_selection(+1)
                else:
                    player = self.game.sprites.sprites()[0]

                    if event.key == pygame.K_LEFT:
                        player.disered_direction = Direction.WEST
                    if event.key == pygame.K_DOWN:
                        player.disered_direction = Direction.SOUTH
                    if event.key == pygame.K_UP:
                        player.disered_direction = Direction.NORTH
                    if event.key == pygame.K_RIGHT:
                        player.disered_direction = Direction.EAST
            if event.type == pygame.QUIT:
                self.running = False



    def run(self) -> None:
        pygame.init()

        self.welcome_menu.show_home_menu(self.screen_width, self.screen_height)
        while self.running:
            if self.menu:
                self.welcome_menu.update()
            else:
                self.game.update()
            self.event()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        pygame.quit()
