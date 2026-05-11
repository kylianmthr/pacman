import pygame

from src.menu_sprites import (
    Text,
    Box,
)


class EndOfGameMenu:
    def __init__(self, engine, type):
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
                    self.engine.screen_height * 0.6,
                ),
            ),
        )
        self.assets.add(
            Box(
                200,
                20,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.7,
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

    def write_name(self):
        pass

    def show(
        self,
    ):
        self.engine.screen.fill("black")
        self.assets.draw(self.engine.screen)

    def event(self, event) -> bool:
        print(event)
        if event.key == pygame.K_RETURN:
            return "return"
        return ""
