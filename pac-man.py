from src.engine import Engine
from src.parser import Parser

if __name__ == "__main__":
    # try:
    parser = Parser("config.json")
    parser.load()
    data = parser.parse()
        # try:
    while True:
        engine = Engine(data)
        engine.run()
        if engine.quit:
            break
        # except Exception as e:
            # print(f"Error running the game: {e}")
    # except Exception as e:
        # print(f"Error loading configuration: {e}")
