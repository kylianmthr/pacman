"""Game engine orchestration for menus, gameplay, and audio."""

import pygame
import os
from typing import Any, cast
import random

from src.models import Config, LevelType
from src.menu import Menu
from src.game import Game
from src.leaderboard import Leaderboard
from src.music import Music


class Engine:
    """Coordinate the main game loop and shared game state."""

    def __init__(self, config: Config) -> None:
        """Initialize engine state from configuration.

        Args:
            config: Parsed game configuration.
        """
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.color = "white"
        self.config = config
        self.menu_active = True
        self.level = 0
        self.loading = False
        self.levels = config.level
        self.fill_levels()
        self.seed = config.seed
        self.running = True
        self.quit = False
        self.music_active = True
        self.score = 0
        self.frame_rate = 60
        self.screen_width = self.levels[self.level].width * 40 + 10
        self.screen_height = self.levels[self.level].height * 40 + 40
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.clock = pygame.time.Clock()
        self.leaderboard = Leaderboard()
        self.menu = Menu(
            self,
        )
        self.game = Game(
            self,
            self.screen,
            self.levels[self.level].width,
            self.levels[self.level].height,
            config.seed,
            config.points_per_pacgum,
            config.points_per_super_pacgum,
            config.points_per_ghost,
            config.lives,
            config.level_max_time,
            config.pacgum,
        )
        self.music = Music(
            "./assets/pacman_beginning.mp3",
            "./assets/eat_dot.wav",
            "./assets/ghost.wav",
            "./assets/pacgum.wav",
        )
        self.music.start_music()

    def fill_levels(self) -> None:
        while len(self.levels) < 10:
            self.levels.append(
                LevelType(
                    width=random.randint(10, 20),
                    height=random.randint(10, 20),
                )
            )

    def change_wall_color(self) -> None:
        """Update all wall sprites to match the current engine color."""
        for wall in self.game.walls:
            typed_wall = cast(Any, wall)
            typed_wall.color = self.color
            typed_wall.image.fill(self.color)

    def next_level(self) -> None:
        """Advance to the next level or show the final menu."""
        if len(self.levels) - 1 == self.level:
            self.menu.switch_menu("game_finished_menu")
        else:
            self.level += 1
            self.screen_width = self.levels[self.level].width * 40 + 10
            self.screen_height = self.levels[self.level].height * 40 + 40
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height)
            )
            self.game = Game(
                self,
                self.screen,
                self.levels[self.level].width,
                self.levels[self.level].height,
                self.seed,
                self.config.points_per_pacgum,
                self.config.points_per_super_pacgum,
                self.config.points_per_ghost,
                self.config.lives,
                self.config.level_max_time,
                self.config.pacgum,
            )
            self.loading = False

    def event(self) -> None:
        """Handle input events and quit requests."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.menu_active:
                    self.menu.event(event)
                else:
                    self.game.event(event)
            if event.type == pygame.QUIT:
                self.quit = True
                self.running = False

    def run(self) -> None:
        """Start the game loop until the engine is stopped."""
        pygame.init()

        while self.running:
            if self.menu_active:
                self.menu.show()
            else:
                self.game.update()
            self.event()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        pygame.quit()
