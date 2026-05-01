from src.engine import Engine

if __name__ == "__main__":
    # parser = Parser("config.json")
    # parser.load()
    # print(parser.parse())
    # maze = generator.MazeGenerator(5, 5, 42, (0, 0), (4, 4))
    # maze.dig()
    engine = Engine(20, 20, 42)
    engine.run()
