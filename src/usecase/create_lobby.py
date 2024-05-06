from pydantic import BaseModel

from src.contract.model import BasicLobbyInfo
from src.domain.redis_connector.record import get_redis_record_template
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.utils import generate_unique_id


class CreateLobbyUseCase(BaseModel):
    redis_handler: RedisHandler

    class Config:
        arbitrary_types_allowed = True
    async def execute(self, admin_id: str, lobby_name: str, max_players: int, number_of_rounds: int) -> BasicLobbyInfo:
        lobby_key = generate_unique_id()

        value = get_redis_record_template()

        value['lobby_metadata']['max_players'] = max_players
        value['lobby_metadata']['number_of_rounds'] = number_of_rounds
        value['lobby_metadata']['lobby_name'] = lobby_name
        value['lobby_metadata']['admin_id'] = admin_id
        value['players'][0]['player_id'] = admin_id

        self.redis_handler.upload_record(str(lobby_key), value)
        return BasicLobbyInfo(
            lobby_id=str(lobby_key),
            lobby_name=lobby_name,
            admin_id=admin_id
        )