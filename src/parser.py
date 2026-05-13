"""Configuration file parser for the game settings."""

from typing import Optional
import json5
from src.models import Config
from pydantic import ValidationError


class Parser:
    """Load and parse a JSON5 configuration file into a Config object."""

    def __init__(self, filename: str) -> None:
        """Initialize the parser with a configuration file path.

        Args:
            filename: Path to the configuration file.
        """
        self.filename = filename
        self.content: Optional[str] = None

    def load(self) -> None:
        """Read the file content and strip comment-only lines."""
        with open(self.filename, "r") as f:
            self.content = f.read()
            lines = self.content.split("\n")
            for i in range(len(lines) - 1):
                if lines[i].strip().startswith("#"):
                    lines.pop(i)
            self.content = "\n".join(lines)

    def parse(self) -> Config:
        """Parse the loaded content into a Config object.

        Returns:
            Parsed configuration model.

        Raises:
            ValueError: If the file is empty or has not been loaded.
        """
        valid_config = {
            "highscore_filename": "test",
            "level": [
                {"width": 10, "height": 10},
                {"width": 10, "height": 10},
            ],
            "lives": 5,
            "pacgum": 5,
            "points_per_pacgum": 5,
            "points_per_super_pacgum": 5,
            "points_per_ghost": 5,
            "seed": 42,
            "level_max_time": 90,
        }
        if self.content:
            try:
                return Config(**json5.loads(self.content))
            except ValidationError as e:
                print("Configuration validation error:", e)
                print("Loading default configuration.")
                return Config(**valid_config)
        raise ValueError("File empty or not loaded")
