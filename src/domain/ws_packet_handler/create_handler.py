import json
import uuid

from starlette.websockets import WebSocket

from src.contract.model import Packet
from src.domain.redis_connector.record import get_redis_record_template
from src.domain.redis_connector.redis_handler import RedisHandler
from src.domain.ws_packet_handler.packet_handler import PacketHandler


class CreateHandler(PacketHandler):

    async def handle_packet(self, packet: Packet, websocket: WebSocket, redis_handler: RedisHandler) -> None:
        print(f"CreateHandler: {packet}")
        lobby_id = uuid.uuid4()
        value = get_redis_record_template()
        redis_handler.upload_record(str(lobby_id), value)
        await websocket.send_json({
            "action": "create",
            "lobby_id": str(lobby_id)
        })

