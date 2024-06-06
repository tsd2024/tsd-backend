from pydantic import BaseModel

from src.database.repository.lobby_history_repository import LobbyHistoryRepository


class LobbyHistoryUseCase(BaseModel):
    lobby_history_repository: LobbyHistoryRepository

    async def execute(self, player_id: str) -> list:
        return self.lobby_history_repository.get_player_lobby_history(player_id)
