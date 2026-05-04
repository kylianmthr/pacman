import pygame
from pygame.math import Vector2
from src.menu_sprites import Button, Picture, Text, TextFromRight, TextFromLeft
from src.models import HighScore, Player
from pathlib import Path
from src.wall import Wall
from src.high_scores import Learderboard


class LeaderBoardMenu:
    def __init__(self, screen, screen_width, screen_height):
        pygame.font.init()
        self.screen = screen
        self.assets = pygame.sprite.Group()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.button_idx = 0
        self.cursors_map = {}
        self.create_static_surfaces()
        self.leader_board = Learderboard()

    def show(self, screen_width, screen_height):
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen.fill("black")
        self.assets.draw(self.screen)

    def stop_menu(self):
        for sprite in self.assets:
            sprite.kill()

    def update_sprite(
        self, sprite: pygame.sprite.Sprite, coordinates: tuple[int, int]
    ):
        sprite.rect = sprite.image.get_rect(center=coordinates)

    def create_static_surfaces(self):
        pacfont = pygame.font.Font("./assets/PAC-FONT.TTF", 35)
        swfont = pygame.font.Font("./assets/Pixelmania.ttf", 15)
        self.assets.add(
            Text(
                "1              9",
                "yellow",
                pacfont,
                (self.screen_width // 2, self.screen_height * 0.1),
            )
        )
        self.assets.add(
            Text(
                "PACMAN",
                "yellow",
                pacfont,
                (self.screen_width // 2, self.screen_height * 0.1),
            )
        )
        self.assets.add(
            Text(
                "22222222222222",
                "yellow",
                pacfont,
                (self.screen_width // 2, self.screen_height * 0.1 + 40),
            )
        )

        self.assets.add(
            Button(
                "RETURN",
                swfont,
                (self.screen_width // 2, self.screen_height * 0.27),
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
        self.assets.add(Wall(5, self.screen_height, (0, 0), "white", "frame"))
        self.assets.add(Wall(self.screen_width, 5, (0, 0), "white", "frame"))
        self.assets.add(
            Wall(
                self.screen_width,
                5,
                (0, self.screen_height - 5),
                "white",
                "frame",
            )
        )
        self.assets.add(
            Wall(
                5,
                self.screen_height,
                (self.screen_width - 5, 0),
                "white",
                "frame",
            )
        )

    def update_leaderboard_surfaces(self, frame_color):
        [pygame.sprite.Sprite.kill(asset) for asset in self.assets]
        self.create_static_surfaces()
        self.leader_board.data_retriever()
        superfunnel = pygame.font.Font("./assets/SuperFunnel.ttf", 25)
        karma_future = pygame.font.Font("./assets/KarmaFuture.ttf", 25)
        coordinate_player_name = Vector2(
            self.screen_width * 0.05, self.screen_height * 0.3
        )
        coordinate_player_score = Vector2(
            self.screen_width * 0.95, self.screen_height * 0.3
        )
        for player in self.leader_board.high_scores.best_players:
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
            frame.image.fill(frame_color)

    # def data_retriever(self):
    #     with open("high_scores.json", "r") as file:
    #         self.high_scores = HighScore.model_validate_json(file.read())

    def event(self, event) -> bool:
        if event.key == pygame.K_RETURN:
            return "return"
        return ""
