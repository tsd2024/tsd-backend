from starlette.websockets import WebSocket

from src.contract.model import Packet
from src.domain.ws_packet_handler.packet_handler import PacketHandler


class CreateHandler(PacketHandler):

    async def handle_packet(self, packet: Packet, websocket: WebSocket) -> None:
        print(f"CreateHandler: {packet}")
        await websocket.send_json("CreateHandler: OK")

