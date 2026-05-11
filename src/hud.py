import pygame
from src.engine import Engine
from src.game import Game
from src.menu_sprites import Text


class HUD:
    def __init__(self, game: Game, engine: Engine):
        self.game = game
        self.engine = engine
        self.arcade_font = pygame.font.Font("./assets/ARCADE_I.TTF", 20)
        self.score = self.Score(
            self,
            str(self.engine.score),
            "white",
            self.arcade_font,
            (20, self.engine.screen_height - 15),
        )
        self.lives = self.Lives(
            self,
            str(self.game.lives),
            "white",
            self.arcade_font,
            (90, self.engine.screen_height - 15),
        )

    class Score(Text):
        def __init__(
            self,
            hud: "HUD",
            text: str,
            color: str,
            font: pygame.font.Font,
            coordinates: tuple[int, int],
        ):
            super().__init__(text, color, font, coordinates)
            self.hud = hud

        def update(self):
            self.text = str(self.hud.engine.score)
            self.image = self.font.render(self.text, True, self.color)

    class Lives(Text):
        def __init__(
            self,
            hud: "HUD",
            text: str,
            color: str,
            font: pygame.font.Font,
            coordinates: tuple[int, int],
        ):
            super().__init__(text, color, font, coordinates)
            self.hud = hud

        def update(self):
            self.text = str(self.hud.game.lives)
            self.image = self.font.render(self.text, True, self.color)
