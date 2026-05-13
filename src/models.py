"""Pydantic models for configuration and leaderboard data."""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class LevelType(BaseModel):
    """Model describing a single level configuration."""

    model_config = ConfigDict(extra="forbid")
    width: int = Field(ge=3)
    height: int = Field(ge=3)


class Config(BaseModel):
    """Configuration model for game settings."""

    model_config = ConfigDict(extra="forbid")
    highscore_filename: str
    level: list[LevelType]
    lives: int = Field(ge=1)
    pacgum: int = Field(ge=0)
    points_per_pacgum: int = Field(ge=0)
    points_per_super_pacgum: int = Field(ge=0)
    points_per_ghost: int = Field(ge=0)
    seed: int
    level_max_time: int = Field(ge=0)


class Player(BaseModel):
    """Leaderboard entry for a player."""

    name: Optional[str] = Field(
        default=None, min_length=1, max_length=10, pattern=r"^[a-zA-Z0-9 ]+$"
    )
    score: int = Field(default=0, ge=0)


class HighScore(BaseModel):
    """Container for the top leaderboard players."""

    best_players: list[Player] = []
