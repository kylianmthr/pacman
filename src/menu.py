import pygame
from typing import Any
from src.leader_board_menu import LeaderBoardMenu
from src.welcome_menu import WelcomeMenu
from src.end_of_game_menu import EndOfGameMenu
from src.menu_sprites import Box, Picture, Button


class HelpMenu:
    def __init__(self, engine: Any, root_menu: Any) -> None:
        self.root_menu = root_menu
        self.engine = engine
        self.assets: Any = pygame.sprite.Group()
        pixelmania = pygame.font.Font("./assets/Pixelmania.ttf", 15)

        self.assets.add(
            Box(
                self.engine.screen_width * 0.98,
                self.engine.screen_height * 0.98,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height // 2,
                ),
                200,
            )
        )
        return_button = Button(
            "RETURN",
            pixelmania,
            (
                self.engine.screen_width // 2,
                self.engine.screen_height * 0.1,
            ),
            1,
            "yellow",
        )
        self.assets.add(return_button)
        self.assets.add(
            Picture(
                "right_selector",
                "./assets/pacman_right.png",
                20,
                20,
                (
                    int(return_button.rect.midright[0] + 15),
                    int(return_button.rect.midright[1]),
                ),
            )
        )
        self.assets.add(
            Picture(
                "left_selector",
                "./assets/pacman_left.png",
                20,
                20,
                (
                    int(return_button.rect.midleft[0] - 15),
                    int(return_button.rect.midleft[1]),
                ),
            )
        )

    def draw(self) -> None:
        self.assets.draw(self.engine.screen)

    def show(
        self,
    ) -> None:
        self.assets.draw(self.engine.screen)

    def event(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_RETURN:
            self.root_menu.switch_menu("welcome_menu")


class Menu:
    def __init__(self, engine: Any) -> None:
        pygame.font.init()
        self.pacfont = pygame.font.Font("./assets/PAC-FONT.TTF", 35)
        self.montserrat = pygame.font.Font("./assets/montserrat.ttf", 15)
        self.pixelmania = pygame.font.Font("./assets/Pixelmania.ttf", 15)
        self.superfunnel = pygame.font.Font("./assets/SuperFunnel.ttf", 20)
        self.karma_future = pygame.font.Font("./assets/KarmaFuture.ttf", 20)
        self.engine = engine
        self.help_menu = HelpMenu(self.engine, self)
        self.game_over_menu = EndOfGameMenu(self.engine, "game_over", self)
        self.game_finished_menu = EndOfGameMenu(
            self.engine, "game_finished", self
        )
        self.welcome_menu = WelcomeMenu(self.engine, self)
        self.mute = False
        self.leaderboard_menu = LeaderBoardMenu(self.engine, self)
        self.current_menu: Any = self.welcome_menu

    def show(self) -> None:
        self.current_menu.show()

    def switch_menu(self, menu_to_switch: str) -> None:
        self.engine.menu_active = True
        if menu_to_switch == "help_menu":
            self.current_menu = self.help_menu
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

    def event(self, event: pygame.event.Event) -> None:
        self.current_menu.event(event)
