from src.contract.model import ActionType
from src.domain.ws_packet_handler.create_handler import CreateHandler
from src.domain.ws_packet_handler.packet_handler import PacketHandler
from src.domain.ws_packet_handler.join_handler import JoinHandler
from src.domain.ws_packet_handler.play_card_handler import PlayCardHandler


class PacketHandlerFactory:
    _HANDLERS = {
        ActionType.CREATE: CreateHandler,
        ActionType.JOIN: JoinHandler,
        ActionType.PLAY_CARD: PlayCardHandler
    }

    def get_handler(self, action_type: ActionType) -> PacketHandler:
        if action_type not in self._HANDLERS:
            raise ValueError(f"Unknown packet type: {action_type}")
        return self._HANDLERS[action_type]()