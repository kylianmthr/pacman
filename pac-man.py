"""Run the Pac-Man game using the configured settings."""

import sys
from src.engine import Engine
from src.parser import Parser

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Invalid arguments")
        parser = Parser(sys.argv[1])
        try:
            parser.load()
        except Exception:
            print("Can't open config file")
        data = parser.parse()
        try:
            while True:
                engine = Engine(data)
                engine.run()
                if engine.quit:
                    break
        except Exception as e:
            print(f"Error running the game: {e}")
    except Exception as e:
        print(f"Error loading configuration: {e}")
