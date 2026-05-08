from src.engine import Engine
from src.parser import Parser

if __name__ == "__main__":
    parser = Parser("config.json")
    parser.load()
    data = parser.parse()
    # maze = generator.MazeGenerator(5, 5, 42, (0, 0), (4, 4))
    # maze.dig()
    engine = Engine(data.level, data.seed)
    engine.run()
