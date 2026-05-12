import pygame
from pygame import Vector2
from src.game import Game
from src.menu_sprites import Box, Text, Button, Picture


class PauseMenu:
    def __init__(self, game: Game, engine):
        self.game = game
        self.engine = engine
        self.assets = pygame.sprite.Group()
        pixelmania = pygame.font.Font("./assets/Pixelmania.ttf", 15)
        print(self.game.engine.screen_width, self.game.engine.screen_height)
        self.assets.add(
            Box(
                self.game.engine.screen_width * 3,
                self.game.engine.screen_height * 3,
                (0, 0),
                200,
            )
        )
        self.assets.add(
            Text(
                "PAUSED",
                "yellow",
                pixelmania,
                (
                    self.game.engine.screen_width // 2,
                    (self.game.engine.screen_height * 0.48) - 50,
                    
                ),
            )
        )
        return_button = Button(
            "RETURN",
            pixelmania,
            (
                self.engine.screen_width // 2,
                self.engine.screen_height * 0.48,
            ),
            1,
            "white",
        )
        self.assets.add(return_button)
        self.assets.add(
            Picture(
                "right_selector",
                "./assets/pacman_right.png",
                20,
                20,
                (Vector2(return_button.rect.midright) + Vector2(15, 0)),
            )
        )
        self.assets.add(
            Picture(
                "left_selector",
                "./assets/pacman_left.png",
                20,
                20,
                (Vector2(return_button.rect.midleft) + Vector2(-15, 0)),
            )
        )

    def draw(self):
        self.assets.draw(self.engine.screen)
