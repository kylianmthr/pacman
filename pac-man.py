from src.parser import Parser

if __name__ == "__main__":
    parser = Parser("config.json")
    parser.load()
    print(parser.parse())
