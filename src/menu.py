import pygame
from src.leader_board_menu import LeaderBoardMenu
from src.welcome_menu import WelcomeMenu
from src.end_of_game_menu import EndOfGameMenu


class Menu:
    def __init__(self, engine):
        pygame.font.init()
        self.pacfont = pygame.font.Font("./assets/PAC-FONT.TTF", 35)
        self.montserrat = pygame.font.Font("./assets/montserrat.ttf", 15)
        self.pixelmania = pygame.font.Font("./assets/Pixelmania.ttf", 15)
        self.superfunnel = pygame.font.Font("./assets/SuperFunnel.ttf", 20)
        self.karma_future = pygame.font.Font("./assets/KarmaFuture.ttf", 20)
        self.engine = engine
        self.game_over_menu = EndOfGameMenu(self.engine, "game_over", self)
        self.game_finished_menu = EndOfGameMenu(
            self.engine, "game_finished", self
        )
        self.welcome_menu = WelcomeMenu(self.engine, self)
        self.mute = False
        self.leaderboard_menu = LeaderBoardMenu(self.engine, self)
        self.current_menu = self.welcome_menu

    def show(self):
        self.current_menu.show()

    def switch_menu(self, menu_to_switch):
        self.engine.menu_active = True
        if menu_to_switch == "leaderboard":
            self.leaderboard_menu.update_leaderboard_surfaces()
            self.current_menu = self.leaderboard_menu
        if menu_to_switch == "welcome_menu":
            self.current_menu = self.welcome_menu
        if menu_to_switch == "game_over_menu":
            self.game_over_menu.display_score()
            self.current_menu = self.game_over_menu
        if menu_to_switch == "game_finished_menu":
            self.game_over_menu.display_score()
            self.current_menu = self.game_finished_menu
        self.current_menu.show()

    def event(self, event):
        self.current_menu.event(event)
