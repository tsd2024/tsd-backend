from starlette.websockets import WebSocket

from src.contract.exceptions import LobbyNotFoundException, NotAdminException, RevealNotReadyException, \
    NextRoundNotReadyException, MaxRoundsReachedException
from src.contract.model import Packet
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.ws_packet_handler.packet_handler import PacketHandler


class NextRoundHandler(PacketHandler):

    async def handle_packet(self, packet: Packet, websocket: WebSocket, redis_handler: RedisHandler) -> None:
        print(f"NextRoundHandler: {packet}")
        player_id = packet.value.get('player_id', None)
        lobby_id = packet.value.get('lobby_id', None)
        if player_id is None:
            await websocket.send_json({
                "action": "next_round_failed",
                "reason": "player_id cannot be None"
            })
            return
        if lobby_id is None:
            await websocket.send_json({
                "action": "next_round_failed",
                "reason": "lobby_id cannot be None"
            })
            return
        try:
            redis_handler.next_round(lobby_id, player_id)
        except LobbyNotFoundException:
            await websocket.send_json({
                "action": "next_round_failed",
                "reason": "Lobby not found"
            })
            return
        except NotAdminException:
            await websocket.send_json({
                "action": "next_round_failed",
                "reason": "Not admin"
            })
            return
        except NextRoundNotReadyException:
            await websocket.send_json({
                "action": "next_round_failed",
                "reason": "Next round not ready"
            })
            return
        except MaxRoundsReachedException:
            await websocket.send_json({
                "action": "next_round_failed",
                "reason": "Max rounds reached"
            })
            return
        await websocket.send_json({
            "action": "next_round_success",
        })
