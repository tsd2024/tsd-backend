from abc import ABC, abstractmethod

from starlette.websockets import WebSocket

from src.contract.model import Packet


class PacketHandler(ABC):
    @abstractmethod
    async def handle_packet(self, packet: Packet, websocket: WebSocket) -> None:
        pass

