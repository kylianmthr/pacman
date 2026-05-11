from src.leader_board_menu import LeaderBoardMenu
from src.welcome_menu import WelcomeMenu
from src.game_over import GameOverMenu


class Menu:
    def __init__(self, engine):
        self.engine = engine
        self.welcome_menu = WelcomeMenu(
            self.engine,
        )
        self.mute = False
        self.leaderboard_menu = LeaderBoardMenu(
            self.engine,
        )
        self.current_menu = self.welcome_menu

    def show(
        self,
    ):
        self.current_menu.show()

    def event(self, event) -> bool:
        menu_result = self.current_menu.event(event)
        if isinstance(self.current_menu, WelcomeMenu):
            if menu_result == "leaderboard":
                self.leaderboard_menu.update_leaderboard_surfaces(
                    self.welcome_menu.frame_color
                )
                self.current_menu = self.leaderboard_menu
            else:
                return menu_result

        elif isinstance(self.current_menu, LeaderBoardMenu):
            if menu_result == "return":
                self.current_menu = self.welcome_menu
        return ""
