from abc import ABC, abstractmethod

from starlette.websockets import WebSocket

from src.contract.model import Packet, Player
from src.domain.redis_connector.redis_handler import RedisHandler


class PacketHandler(ABC):
    @abstractmethod
    async def handle_packet(self, packet: Packet, websocket: WebSocket, redis_handler: RedisHandler) -> None | Player:
        pass

