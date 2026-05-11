import pygame
from pygame.math import Vector2
from src.menu_sprites import Button, Picture, Text, TextFromRight, TextFromLeft
from src.wall import Wall


class LeaderBoardMenu:
    def __init__(self, engine, root_menu):
        self.root_menu = root_menu
        self.engine = engine
        pygame.font.init()
        self.assets = pygame.sprite.Group()
        self.buttons = []
        self.button_idx = 0
        self.cursors_map = {}
        self.create_static_surfaces()

    def show(
        self,
    ):
        self.engine.screen.fill("black")
        self.assets.draw(self.engine.screen)

    def update_sprite(
        self, sprite: pygame.sprite.Sprite, coordinates: tuple[int, int]
    ):
        sprite.rect = sprite.image.get_rect(center=coordinates)

    def create_static_surfaces(self):
        pacfont = pygame.font.Font("./assets/PAC-FONT.TTF", 35)
        pixelmania = pygame.font.Font("./assets/Pixelmania.ttf", 15)
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
            Button(
                "RETURN",
                pixelmania,
                (
                    self.engine.screen_width // 2,
                    self.engine.screen_height * 0.27,
                ),
                1,
                "yellow",
            )
        )
        self.buttons = [
            button for button in self.assets if isinstance(button, Button)
        ]
        self.cursors_map = {
            button.name: {
                "left": Vector2(button.rect.midleft),
                "right": Vector2(button.rect.midright),
            }
            for button in self.buttons
        }
        self.assets.add(
            Picture(
                "right_selector",
                "./assets/pacman_right.png",
                20,
                20,
                (
                    (
                        self.cursors_map[self.buttons[self.button_idx].name][
                            "right"
                        ]
                    )
                    + Vector2(15, 0)
                ),
            )
        )
        self.assets.add(
            Picture(
                "left_selector",
                "./assets/pacman_left.png",
                20,
                20,
                (self.cursors_map[self.buttons[self.button_idx].name]["left"])
                + Vector2(-15, 0),
            )
        )
        self.assets.add(
            Wall(5, self.engine.screen_height, (0, 0), "white", "frame")
        )
        self.assets.add(
            Wall(self.engine.screen_width, 5, (0, 0), "white", "frame")
        )
        self.assets.add(
            Wall(
                self.engine.screen_width,
                5,
                (0, self.engine.screen_height - 5),
                "white",
                "frame",
            )
        )
        self.assets.add(
            Wall(
                5,
                self.engine.screen_height,
                (self.engine.screen_width - 5, 0),
                "white",
                "frame",
            )
        )

    def update_leaderboard_surfaces(self):
        [pygame.sprite.Sprite.kill(asset) for asset in self.assets]
        self.create_static_surfaces()
        self.engine.leaderboard.data_retriever()
        superfunnel = pygame.font.Font("./assets/SuperFunnel.ttf", 25)
        karma_future = pygame.font.Font("./assets/KarmaFuture.ttf", 25)
        coordinate_player_name = Vector2(
            self.engine.screen_width * 0.05, self.engine.screen_height * 0.3
        )
        coordinate_player_score = Vector2(
            self.engine.screen_width * 0.95, self.engine.screen_height * 0.3
        )
        for player in self.engine.leaderboard.high_scores.best_players:
            if player.score > 0:
                coordinate_player_name += Vector2(0, 30)
                coordinate_player_score += Vector2(0, 30)
                self.assets.add(
                    TextFromLeft(
                        f"{player.name}",
                        "yellow",
                        superfunnel,
                        coordinate_player_name,
                    )
                )
                if player.score > 9999999999999:
                    self.assets.add(
                        TextFromRight(
                            "Game finished",
                            "yellow",
                            karma_future,
                            coordinate_player_score,
                        )
                    )
                else:
                    self.assets.add(
                        TextFromRight(
                            f"{player.score}",
                            "yellow",
                            karma_future,
                            coordinate_player_score,
                        )
                    )
        frames = [frame for frame in self.assets if frame.name == "frame"]
        for frame in frames:
            frame.image.fill(self.engine.color)

    def event(self, event) -> bool:
        if event.key == pygame.K_RETURN:
            self.root_menu.switch_menu("welcome_menu")
