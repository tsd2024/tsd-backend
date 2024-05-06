from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter

from src.app.container import Container
from src.app.request.create_lobby import CreateLobbyRequest
from src.app.response.create_lobby import CreateLobbyResponse
from src.usecase.create_lobby import CreateLobbyUseCase

api = APIRouter()

@api.post("/create")
@inject
async def create_lobby(
        request: CreateLobbyRequest,
        use_case: CreateLobbyUseCase = Depends(Provide(Container.create_lobby_use_case))
) -> CreateLobbyResponse:

    lobby_info = await use_case.execute(
        admin_id=request.admin_id,
        lobby_name=request.lobby_name,
        max_players=request.max_players,
        number_of_rounds=request.number_of_rounds
    )

    return CreateLobbyResponse(
        lobby_id=lobby_info.lobby_id,
        lobby_name=lobby_info.lobby_name,
        admin_id=lobby_info.admin_id
    )


