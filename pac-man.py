from src.engine import Engine
from src.parser import Parser

if __name__ == "__main__":
    try:
        parser = Parser("config.json")
        parser.load()
        data = parser.parse()
        try:
            # maze = generator.MazeGenerator(5, 5, 42, (0, 0), (4, 4))
            # maze.dig()
            engine = Engine(data)
            engine.run()
        except Exception as e:
            print(f"Error running the game: {e}")
    except Exception as e:
        print(f"Error loading configuration: {e}")
