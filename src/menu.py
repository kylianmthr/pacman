from src.leader_board_menu import LeaderBoardMenu
from src.welcome_menu import WelcomeMenu
from src.game_over_menu import EndOfGameMenu


class Menu:
    def __init__(self, engine):
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
        if menu_to_switch == "leaderboard":
            self.leaderboard_menu.update_leaderboard_surfaces()
            self.current_menu = self.leaderboard_menu
        if menu_to_switch == "welcome_menu":
            self.current_menu = self.welcome_menu
        if menu_to_switch == "game_over_menu":
            self.current_menu = self.game_over_menu
        if menu_to_switch == "game_finished_menu":
            self.current_menu = self.game_finished_menu
        self.current_menu.show()

    def event(self, event):
        self.current_menu.event(event)
