

from starlette.websockets import WebSocket

from src.contract.exceptions import LobbyNotFoundException, PlayerNotFoundException, CardNotAvailableException
from src.contract.model import Packet
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.ws_packet_handler.packet_handler import PacketHandler

class PlayCardHandler(PacketHandler):

    async def handle_packet(self, packet: Packet, websocket: WebSocket, redis_handler: RedisHandler) -> None:
        print(f"PlayCardHandler: {packet}")

        player_id = packet.value.get('player_id', None)
        lobby_id = packet.value.get('lobby_id', None)
        card = packet.value.get('card', None)
        if player_id is None:
            await websocket.send_json({
                "action": "play_card_failed",
                "reason": "player_id cannot be None"
            })
            return
        if lobby_id is None:
            await websocket.send_json({
                "action": "play_card_failed",
                "reason": "lobby_id cannot be None"
            })
            return
        if card is None:
            await websocket.send_json({
                "action": "play_card_failed",
                "reason": "card cannot be None"
            })
            return

        try:
            redis_handler.play_card(lobby_id, player_id, card)
        except LobbyNotFoundException:
            await websocket.send_json({
                "action": "play_card_failed",
                "reason": "Lobby not found"
            })
            return
        except PlayerNotFoundException:
            await websocket.send_json({
                "action": "play_card_failed",
                "reason": "Player not found"
            })
            return
        except CardNotAvailableException:
            await websocket.send_json({
                "action": "play_card_failed",
                "reason": "Card not available"
            })
            return
        await websocket.send_json({
            "action": "play_card_success",
        })

