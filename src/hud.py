"""Heads-up display sprites for score, lives, timer, and level."""

import pygame
from src.engine import Engine
from src.game import Game
from src.menu_sprites import TextFromLeft


class HUD:
    """Container for HUD text sprites and their updates."""

    def __init__(self, game: Game, engine: Engine) -> None:
        """Initialize HUD sprites.

        Args:
            game: Game instance providing gameplay state.
            engine: Engine instance providing global state.
        """
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
        """Text sprite for the score display."""

        def __init__(
            self,
            hud: "HUD",
            text: str,
            color: str,
            font: pygame.font.Font,
            coordinates: tuple[int, int],
        ) -> None:
            """Initialize the score sprite.

            Args:
                hud: Owning HUD instance.
                text: Initial text content.
                color: Text color.
                font: Font used for rendering.
                coordinates: Left-aligned coordinates.
            """
            super().__init__(text, color, font, coordinates)
            self.hud = hud

        def update(self) -> None:
            """Update the score text based on current points."""
            score = self.hud.engine.score
            self.text = f"SCORE  {str(score) if score <= 9999 else '9999'}"
            self.image = self.font.render(self.text, True, self.color)

    class Lives(TextFromLeft):
        """Text sprite for the remaining lives display."""

        def __init__(
            self,
            hud: "HUD",
            text: str,
            color: str,
            font: pygame.font.Font,
            coordinates: tuple[int, int],
        ) -> None:
            """Initialize the lives sprite.

            Args:
                hud: Owning HUD instance.
                text: Initial text content.
                color: Text color.
                font: Font used for rendering.
                coordinates: Left-aligned coordinates.
            """
            super().__init__(text, color, font, coordinates)
            self.hud = hud

        def update(self) -> None:
            """Update the lives text based on current lives."""
            self.text = f"LIVES  {str(self.hud.game.lives)}"
            self.rect.x = self.hud.score.get_size()[0] + 10 * 2
            self.image = self.font.render(self.text, True, self.color)

    class Timer(TextFromLeft):
        """Text sprite for the remaining time display."""

        def __init__(
            self,
            hud: "HUD",
            text: str,
            color: str,
            font: pygame.font.Font,
            coordinates: tuple[int, int],
        ) -> None:
            """Initialize the timer sprite.

            Args:
                hud: Owning HUD instance.
                text: Initial text content.
                color: Text color.
                font: Font used for rendering.
                coordinates: Left-aligned coordinates.
            """
            super().__init__(text, color, font, coordinates)
            self.hud = hud

        def update(self) -> None:
            """Update the timer text based on remaining time."""
            self.text = f"TIMER  {str(self.hud.game.timer.current_time())}"
            self.rect.x = (
                self.hud.score.get_size()[0]
                + self.hud.lives.get_size()[0]
                + 10 * 3
            )
            self.image = self.font.render(self.text, True, self.color)

    class Level(TextFromLeft):
        """Text sprite for the current level display."""

        def __init__(
            self,
            hud: "HUD",
            text: str,
            color: str,
            font: pygame.font.Font,
            coordinates: tuple[int, int],
        ) -> None:
            """Initialize the level sprite.

            Args:
                hud: Owning HUD instance.
                text: Initial text content.
                color: Text color.
                font: Font used for rendering.
                coordinates: Left-aligned coordinates.
            """
            super().__init__(text, color, font, coordinates)
            self.hud = hud

        def update(self) -> None:
            """Update the level text based on current level."""
            self.text = f"LEVEL  {str(self.hud.game.engine.level + 1)}"
            self.rect.x = (
                self.hud.score.get_size()[0]
                + self.hud.lives.get_size()[0]
                + self.hud.timer.get_size()[0]
                + 10 * 4
            )
            self.image = self.font.render(self.text, True, self.color)
