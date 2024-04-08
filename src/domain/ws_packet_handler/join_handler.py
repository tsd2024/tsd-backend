import json
import uuid
import random

from starlette.websockets import WebSocket

from src.contract.model import Packet
from src.domain.redis_connector.record import get_redis_record_template, get_player_template
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.ws_packet_handler.packet_handler import PacketHandler


class NoPlayerIdException(Exception):
    pass

class JoinHandler(PacketHandler):

    async def handle_packet(self, packet: Packet, websocket: WebSocket, redis_handler: RedisHandler) -> None:
        print(f"JoinHandler: {packet}")

        # get redis record to update, for now it is just a template.
        value = get_player_template()

        player_id = packet.value.get('player_id', None)
        if player_id is None:
            raise NoPlayerIdException("player_id cannot be None")
        value['player_id'] = player_id


        redis_handler.upload_record(str(player_id), value)
        await websocket.send_json({
            "action": "join",
            "player_id": str(player_id)
        })

