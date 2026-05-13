"""High score persistence and ranking logic."""

from pathlib import Path
from pydantic import TypeAdapter
from src.models import HighScore, Player


class Leaderboard:
    """Manage leaderboard data and persistence."""

    def __init__(self, file_name: str) -> None:
        """Initialize leaderboard data and load existing scores."""
        self.file_name = file_name
        self.high_scores = HighScore()
        self.source_list_adapter = TypeAdapter(HighScore)
        self.data_retriever()

    def rank_player(self, player: Player) -> None:
        """Insert a player into the leaderboard and persist results.

        Args:
            player: Player entry to rank.
        """
        self.data_retriever()
        self.high_scores.best_players.append(player)
        self.high_scores.best_players.sort(
            key=lambda player: player.score, reverse=True
        )
        self.high_scores.best_players = self.high_scores.best_players[:10]
        with open(f"{self.file_name}", "wb") as file:
            file.write(
                self.source_list_adapter.dump_json(self.high_scores, indent=4)
            )

    def create_json(self) -> None:
        """Create a default leaderboard file with empty player slots."""
        for i in range(10):
            player = Player()
            self.high_scores.best_players.append(player)
        with open(f"{self.file_name}", "wb") as file:
            file.write(
                self.source_list_adapter.dump_json(self.high_scores, indent=4)
            )

    def data_retriever(self) -> None:
        """Load leaderboard data or create default storage."""
        path = Path(f"{self.file_name}")
        if not path.exists():
            self.create_json()
        else:
            try:
                with open(f"{self.file_name}", "r") as file:
                    self.high_scores = HighScore.model_validate_json(
                        file.read()
                    )
                    self.high_scores.best_players.sort(
                        key=lambda player: player.score, reverse=True
                    )
                    self.high_scores.best_players = (
                        self.high_scores.best_players[:10]
                    )
            except Exception:
                self.create_json()
