from src.contract.model import ActionType
from src.domain.ws_packet_handler.create_handler import CreateHandler
from src.domain.ws_packet_handler.packet_handler import PacketHandler


class PacketHandlerFactory:
    _HANDLERS = {
        ActionType.CREATE: CreateHandler
    }

    def get_handler(self, action_type: ActionType) -> PacketHandler:
        if action_type not in self._HANDLERS:
            raise ValueError(f"Unknown packet type: {action_type}")
        return self._HANDLERS[action_type]()