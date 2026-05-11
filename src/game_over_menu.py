import pygame

from src.menu_sprites import (
    Text,
    Box,
)
from src.models import Player


class EndOfGameMenu:
    def __init__(self, engine, type, root_menu):
        self.root_menu = root_menu
        self.player_name = ""
        self.player_name_display = None
        self.type = type
        self.engine = engine
        pygame.font.init()
        self.assets = pygame.sprite.Group()
        self.create_static_surfaces()

    def create_static_surfaces(self):
        pacfont = pygame.font.Font("./assets/PAC-FONT.TTF", 35)
        montserrat = pygame.font.Font("./assets/montserrat.ttf", 15)
        self.assets.add(
            Text(
                "1              9",
                "yellow",
                pacfont,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.1,
                ),
            )
        )
        self.assets.add(
            Text(
                "PACMAN",
                "yellow",
                pacfont,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.1,
                ),
            )
        )
        self.assets.add(
            Text(
                "22222222222222",
                "yellow",
                pacfont,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.1 + 40,
                ),
            )
        )
        self.assets.add(
            Text(
                "Enter your name :",
                "white",
                montserrat,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.7,
                ),
            ),
        )

        self.assets.add(
            Box(
                200,
                20,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.8,
                ),
            )
        )
        if self.type == "game_over":
            self.assets.add(
                Text(
                    "GAME OVER",
                    "yellow",
                    pacfont,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.4,
                    ),
                ),
            )
        elif self.type == "game_finished":
            self.assets.add(
                Text(
                    "GAME FINISHED",
                    "yellow",
                    pacfont,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.4,
                    ),
                ),
                Text(
                    "WELL DONE !",
                    "yellow",
                    montserrat,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.5,
                    ),
                ),
            )
        self.player_name_display = Text(
            self.player_name,
            "black",
            montserrat,
            (
                self.engine.screen_width // 2,
                self.engine.screen_height * 0.8,
            ),
        )
        self.assets.add(self.player_name_display)

    def show(
        self,
    ):

        self.engine.screen.fill("black")
        self.write_player_score()
        self.assets.draw(self.engine.screen)

    def write_player_score(self):
        montserrat = pygame.font.Font("./assets/montserrat.ttf", 15)
        self.player_name_display.image = montserrat.render(
            self.player_name, True, "black", None
        )
        self.player_name_display.rect = (
            self.player_name_display.image.get_rect(
                center=self.player_name_display.coordinates
            )
        )
        if self.engine.score > 9999999999999:
            self.assets.add(
                Text(
                    "Maximum score",
                    "white",
                    montserrat,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.6,
                    ),
                ),
            )
        else:
            self.assets.add(
                Text(
                    f"your score is {self.engine.score} points",
                    "white",
                    montserrat,
                    (
                        self.engine.screen_width // 2,
                        self.engine.screen_height * 0.6,
                    ),
                ),
            )

    def event(self, event) -> bool:
        if (event.unicode.isalnum() or event.unicode == " ") and len(
            self.player_name
        ) < 10:
            self.player_name = self.player_name + event.unicode
            self.write_player_score()
            self.show()
        if event.key == 8 and len(self.player_name) > 0:
            self.player_name = self.player_name[: len(self.player_name) - 1]
        if event.key == pygame.K_RETURN and len(self.player_name) > 0:
            self.engine.leaderboard.rank_player(
                Player(name=self.player_name, score=self.engine.score)
            )
            self.root_menu.switch_menu("welcome_menu")
