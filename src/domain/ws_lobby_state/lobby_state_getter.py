from starlette.websockets import WebSocket

from src.contract.exceptions import RevealNotReadyException
from src.domain.redis_connector.redis_handler import RedisHandler


class LobbyStateGetter:
    async def get_lobby_status(self, lobby_key: str, player_id: int, websocket: WebSocket,
                               redis_handler: RedisHandler):
        try:
            cards = redis_handler.get_lobby_status(lobby_key)
        except RevealNotReadyException:
            return
        await websocket.send_json({
            "action": "lobby_state",
            "value": cards
        })
