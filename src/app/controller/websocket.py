import asyncio

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, WebSocket

from src.app.container import Container
from src.contract.model import ActionType, Packet
from src.contract.exceptions import InvalidTokenException, MissingTokenException
from src.domain.ws_packet_handler.packet_handler_factory import PacketHandlerFactory

api = APIRouter()


@api.websocket('/room')
@inject
async def websocket_endpoint(
        websocket: WebSocket,
        packet_handler_factory: PacketHandlerFactory = Depends(Provide(Container.packet_handler_factory)),
        redis_handler=Depends(Provide(Container.redis_handler)),
        lobby_state_getter=Depends(Provide(Container.lobby_state_getter)),
        token_verifier=Depends(Provide(Container.token_verifier)),
        history_saver=Depends(Provide(Container.history_saver))
):
    await websocket.accept()
    # try:
    #     token = websocket.query_params.get("token", "")
    #     user_info = token_verifier.verify_token(token)
    # except (InvalidTokenException, MissingTokenException) as e:
    #     await websocket.send_text(str(e))
    #     await websocket.close()
    #     return
    lobby_key = None
    player_id = None
    while True:
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=1)
        except asyncio.TimeoutError:
            if lobby_key and player_id:
                await lobby_state_getter.get_lobby_status(lobby_key, player_id, websocket, redis_handler)
            continue
        action_type = ActionType(data.get('action'))

        handler = packet_handler_factory.get_handler(action_type)
        packet = Packet(action=action_type, value=data.get('value'))
        if action_type == ActionType.CREATE or action_type == ActionType.JOIN:
            player = await handler.handle_packet(packet, websocket, redis_handler)
            if player:
                lobby_key = player.lobby_key
                player_id = player.player_id
        else:
            await handler.handle_packet(packet, websocket, redis_handler)
        await history_saver.save_lobby_history(lobby_key, player_id, redis_handler)


