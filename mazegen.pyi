class generator:
    class MazeGenerator:
        maze: list[list[str]]
        forty_two_cell: list[tuple[int, int]]
        entry: tuple[int, int]
        exit: tuple[int, int]

        def __init__(
            self,
            width: int,
            height: int,
            seed: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
        ) -> None: ...

        def generate(self, start: tuple[int, int]) -> None: ...
        def dig(self) -> None: ...
        def solve(self) -> object: ...
        def parser(self, solution: object) -> list[str]: ...
