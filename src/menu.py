import pygame
from pygame.math import Vector2
from src.menu_sprites import Button, Picture, Text
from src.leader_board_menu import LeaderBoardMenu
from src.welcome_menu import WelcomeMenu


class Menu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.welcome_menu = WelcomeMenu(screen, screen_width, screen_height)
        self.mute = False
        self.leaderboard_menu = LeaderBoardMenu(
            screen, screen_width, screen_height
        )
        self.current_menu = self.welcome_menu

    def show(self, screen_width, screen_height):
        self.current_menu.show(screen_width, screen_height)

    def event(self, event) -> bool:
        menu_result = self.current_menu.event(event)
        if isinstance(self.current_menu, WelcomeMenu):
            if menu_result == "leaderboard":
                self.leaderboard_menu.update_leaderboard_surfaces()
                self.current_menu = self.leaderboard_menu
            else:
                return menu_result

        elif isinstance(self.current_menu, LeaderBoardMenu):
            if menu_result == "return":
                self.current_menu = self.welcome_menu

        return True
