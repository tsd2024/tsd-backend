import json
import uuid
import random

from starlette.websockets import WebSocket

from src.contract.model import Packet
from src.domain.redis_connector.record import get_redis_record_template
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.ws_packet_handler.packet_handler import PacketHandler

class NoAdminIdException(Exception):
    pass
class CreateHandler(PacketHandler):

    async def handle_packet(self, packet: Packet, websocket: WebSocket, redis_handler: RedisHandler) -> None:
        print(f"CreateHandler: {packet}")

        lobby_id = generate_unique_id()

        value = get_redis_record_template()

        max_players = packet.value.get('max_players', 5)
        value['lobby_metadata']['max_players'] = max_players

        number_of_rounds = packet.value.get('number_of_rounds', 5)
        value['lobby_metadata']['number_of_rounds'] = number_of_rounds

        lobby_name = packet.value.get('lobby_name', "")
        value['lobby_metadata']['lobby_name'] = lobby_name

        admin_id = packet.value.get('admin_id', None)
        if admin_id is None:
            raise NoAdminIdException("admin_id cannot be None.")
        value['lobby_metadata']['admin_id'] = admin_id
        value['players'][0]['player_id'] = admin_id

        redis_handler.upload_record(str(lobby_id), value)
        await websocket.send_json({
            "action": "create",
            "lobby_id": str(lobby_id),
            "admin_id": str(admin_id)
        })

def generate_unique_id():
    return '-'.join(str(random.randint(100, 999)) for _ in range(2))
