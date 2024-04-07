from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, WebSocket

from src.app.container import Container
from src.contract.model import ActionType, Packet
from src.domain.ws_packet_handler.packet_handler_factory import PacketHandlerFactory

api = APIRouter()

@api.websocket('/room')
@inject
async def websocket_endpoint(
        websocket: WebSocket,
        packet_handler_factory: PacketHandlerFactory = Depends(Provide(Container.packet_handler_factory)),
        redis_handler = Depends(Provide(Container.redis_handler))
        ):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        action_type = ActionType(data.get('action'))
        handler = packet_handler_factory.get_handler(action_type)
        packet = Packet(action = action_type, value = data.get('value'))
        await handler.handle_packet(packet, websocket, redis_handler)
