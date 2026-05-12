import pygame
from src.game import Game
from src.menu_sprites import Box, Text


class PauseMenu:
    def __init__(self, game: Game, screen):
        self.game = game
        self.screen = screen
        self.sprites = pygame.sprite.Group()
        pixelmania = pygame.font.Font("./assets/Pixelmania.ttf", 15)
        self.sprites.add(
            Box(
                self.game.engine.screen_width * 3,
                self.game.engine.screen_height * 3,
                (0, 0),
                200,
            )
        )
        self.sprites.add(
            Text(
                "PAUSED",
                "yellow",
                pixelmania,
                (
                    self.game.engine.screen_width // 2,
                    self.game.engine.screen_height // 2 - 50,
                ),
            )
        )

    def evt(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.timer.toggle_pause()

    def draw(self):
        self.sprites.draw(self.screen)
