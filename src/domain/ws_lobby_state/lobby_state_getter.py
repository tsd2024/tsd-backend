from starlette.websockets import WebSocket

from src.contract.exceptions import RevealNotReadyException, PlayerNotFoundException, LobbyNotFoundException
from src.domain.redis_connector.redis_handler import RedisHandler


class LobbyStateGetter:
    async def get_lobby_status(self, lobby_key: str, player_id: int, websocket: WebSocket,
                               redis_handler: RedisHandler):
        try:
            sync_result = redis_handler.sync_player_round_number(lobby_key, player_id)
            if sync_result:
                await websocket.send_json({
                    "action": "next_round",
                })
        except (PlayerNotFoundException, LobbyNotFoundException):
            pass
        try:
            cards = redis_handler.get_lobby_status(lobby_key)
        except (RevealNotReadyException, LobbyNotFoundException):
            return
        await websocket.send_json({
            "action": "lobby_state",
            "value": cards
        })
