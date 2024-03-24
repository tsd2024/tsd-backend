from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, WebSocket

from src.app.container import Container
from src.contract.model import ActionType
from src.domain.ws_packet_handler.packet_handler_factory import PacketHandlerFactory

api = APIRouter()

@api.websocket('/room')
@inject
async def websocket_endpoint(
        websocket: WebSocket,
        packet_handler_factory: PacketHandlerFactory = Depends(Provide(Container.packet_handler_factory))
        ):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        action_type = ActionType(data.get('action'))
        handler = packet_handler_factory.get_handler(action_type)
        await handler.handle_packet(data, websocket)
