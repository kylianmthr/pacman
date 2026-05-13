"""Configuration file parser for the game settings."""

from typing import Optional
import json5
from src.models import Config


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
        if self.content:
            return Config(**json5.loads(self.content))
        raise ValueError("File empty or not loaded")
