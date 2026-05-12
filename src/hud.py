# mypy: ignore-errors
import pygame
from src.engine import Engine
from src.game import Game
from src.menu_sprites import TextFromLeft


class HUD:
    def __init__(self, game: Game, engine: Engine):
        self.game = game
        self.engine = engine
        self.arcade_font = pygame.font.Font("./assets/Pixelmania.ttf", 8)
        self.score = self.Score(
            self,
            f"SCORE  {str(self.engine.score)}",
            "white",
            self.arcade_font,
            (10, self.engine.screen_height - 15),
        )
        self.lives = self.Lives(
            self,
            f"LIVES  {str(self.game.lives)}",
            "white",
            self.arcade_font,
            (
                self.score.get_size()[0] + 5 * 2,
                self.engine.screen_height - 15,
            ),
        )
        self.timer = self.Timer(
            self,
            f"TIMER  {str(self.game.timer.current_time())}",
            "white",
            self.arcade_font,
            (
                self.score.get_size()[0] + self.lives.get_size()[0] + 10 * 4,
                self.engine.screen_height - 15,
            ),
        )
        self.level = self.Level(
            self,
            f"LEVEL  {str(self.game.engine.level)}",
            "white",
            self.arcade_font,
            (
                self.score.get_size()[0]
                + self.lives.get_size()[0]
                + self.timer.get_size()[0]
                + 10 * 4,
                self.engine.screen_height - 15,
            ),
        )

    class Score(TextFromLeft):
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
            score = self.hud.engine.score
            self.text = f"SCORE  {str(score) if score <= 9999 else '9999'}"
            self.image = self.font.render(self.text, True, self.color)

    class Lives(TextFromLeft):
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
            self.text = f"LIVES  {str(self.hud.game.lives)}"
            self.rect.x = self.hud.score.get_size()[0] + 10 * 2
            self.image = self.font.render(self.text, True, self.color)

    class Timer(TextFromLeft):
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
            self.text = f"TIMER  {str(self.hud.game.timer.current_time())}"
            self.rect.x = (
                self.hud.score.get_size()[0]
                + self.hud.lives.get_size()[0]
                + 10 * 3
            )
            self.image = self.font.render(self.text, True, self.color)

    class Level(TextFromLeft):
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
            self.text = f"LEVEL  {str(self.hud.game.engine.level + 1)}"
            self.rect.x = (
                self.hud.score.get_size()[0]
                + self.hud.lives.get_size()[0]
                + self.hud.timer.get_size()[0]
                + 10 * 4
            )
            self.image = self.font.render(self.text, True, self.color)
