from pydantic import BaseModel

from src.database.repository.lobby_history_repository import LobbyHistoryRepository
from src.domain.redis_connector.redis_handler import RedisHandler


class HistorySaver(BaseModel):
    lobby_history_repository: LobbyHistoryRepository

    async def save_lobby_history(self, lobby_id: str, player_id: str, redis_handler: RedisHandler) -> None:
        lobby_metadata = redis_handler.get_lobby_status(lobby_id)
        lobby_metadata.pop('round_number')
        lobby_metadata.pop('reveal_ready')
        lobby_metadata.pop('current_user_story_id')
        admin_id = str(lobby_metadata.get('admin_id'))
        if admin_id != player_id:
            return

        players = lobby_metadata.get('players')
        for player in players:
            id = str(player.get('player_id'))
            self.lobby_history_repository.add_or_update_lobby_history(lobby_id, id, lobby_metadata)
