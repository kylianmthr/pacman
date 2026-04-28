from typing import Optional
import json5
from src.models import Config


class Parser:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.content: Optional[str] = None

    def load(self) -> None:
        with open(self.filename, "r") as f:
            self.content = f.read()
            lines = self.content.split("\n")
            for i in range(len(lines) - 1):
                print(i)
                if lines[i].strip().startswith("#"):
                    lines.pop(i)
            self.content = "\n".join(lines)
            print(self.content)

    def parse(self) -> Config:
        if self.content:
            return Config(**json5.loads(self.content))
        raise ValueError("File empty or not loaded")
