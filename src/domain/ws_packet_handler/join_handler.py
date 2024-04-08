
from starlette.websockets import WebSocket

from src.contract.model import Packet, Player
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.ws_packet_handler.packet_handler import PacketHandler

from src.domain.redis_connector.redis_handler import MaxPlayersReachedException


class NoPlayerIdException(Exception):
    pass

class NoLobbyIdException(Exception):
    pass

class JoinHandler(PacketHandler):

    async def handle_packet(self, packet: Packet, websocket: WebSocket, redis_handler: RedisHandler) -> None | Player:
        print(f"JoinHandler: {packet}")

        player_id = packet.value.get('player_id', None)
        lobby_key = packet.value.get('lobby_id', None)
        if player_id is None:
            await websocket.send_json({
                "action": "join_failed",
                "reason": "player_id cannot be None"
            })
            return
        if lobby_key is None:
            await websocket.send_json({
                "action": "join_failed",
                "reason": "lobby_id cannot be None"
            })
            return


        try:
            redis_handler.join_lobby(lobby_key, player_id)
        except MaxPlayersReachedException as e:
            await websocket.send_json({
                "action": "join_failed",
                "reason": "max players reached",
            })
            return
        await websocket.send_json({
            "action": "join_success",
        })
        return Player(player_id=str(player_id), lobby_key=lobby_key)
