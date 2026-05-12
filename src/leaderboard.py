from pathlib import Path
from pydantic import TypeAdapter
from src.models import HighScore, Player


class Leaderboard:
    def __init__(self) -> None:
        self.high_scores = HighScore()
        self.source_list_adapter = TypeAdapter(HighScore)
        self.data_retriever()

    def rank_player(self, player: Player) -> None:
        self.data_retriever()
        self.high_scores.best_players.append(player)
        self.high_scores.best_players.sort(
            key=lambda player: player.score, reverse=True
        )
        self.high_scores.best_players = self.high_scores.best_players[:10]
        with open("high_scores.json", "wb") as file:
            file.write(
                self.source_list_adapter.dump_json(self.high_scores, indent=4)
            )

    def create_json(self) -> None:
        for i in range(10):
            player = Player()
            self.high_scores.best_players.append(player)
        with open("high_scores.json", "wb") as file:
            file.write(
                self.source_list_adapter.dump_json(self.high_scores, indent=4)
            )

    def data_retriever(self) -> None:
        path = Path("high_scores.json")
        if not path.exists():
            self.create_json()
        else:
            with open("high_scores.json", "r") as file:
                self.high_scores = HighScore.model_validate_json(file.read())
                self.high_scores.best_players.sort(
                    key=lambda player: player.score, reverse=True
                )
                self.high_scores.best_players = self.high_scores.best_players[
                    :10
                ]
