from starlette.websockets import WebSocket

from src.contract.exceptions import CancelNotAvailableException, PlayerNotFoundException, LobbyNotFoundException
from src.contract.model import Packet, Player
from src.domain.redis_connector.redis_handler import MaxPlayersReachedException
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.ws_packet_handler.packet_handler import PacketHandler


class CancelHandler(PacketHandler):

    async def handle_packet(self, packet: Packet, websocket: WebSocket, redis_handler: RedisHandler) -> None:
        print(f"CancelHandler: {packet}")

        player_id = packet.value.get('player_id', None)
        lobby_key = packet.value.get('lobby_id', None)
        if player_id is None:
            await websocket.send_json({
                "action": "cancel_failed",
                "reason": "player_id cannot be None"
            })
            return
        if lobby_key is None:
            await websocket.send_json({
                "action": "cancel_failed",
                "reason": "lobby_id cannot be None"
            })
            return

        try:
            redis_handler.cancel_choice(lobby_key, player_id)
        except CancelNotAvailableException:
            await websocket.send_json({
                "action": "cancel_failed",
                "reason": "cancel not available"
            })
            return
        except PlayerNotFoundException:
            await websocket.send_json({
                "action": "cancel_failed",
                "reason": "player not found"
            })
            return
        except LobbyNotFoundException:
            await websocket.send_json({
                "action": "cancel_failed",
                "reason": "lobby not found"
            })
            return
        await websocket.send_json({
            "action": "cancel_success",
        })
