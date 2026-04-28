from src.parser import Parser
from src.engine import Engine
from mazegen import generator

if __name__ == "__main__":
    # parser = Parser("config.json")
    # parser.load()
    # print(parser.parse())
    # maze = generator.MazeGenerator(5, 5, 42, (0, 0), (4, 4))
    # maze.dig()
    engine = Engine()
    engine.run()
