from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.app.container import Container
from src.domain.google_auth.token_verifier_request import verify_token
from src.usecase.get_lobby_history import LobbyHistoryUseCase

api = APIRouter()


@api.get("/lobby_history")
@inject
async def get_lobby_history(
        use_case: LobbyHistoryUseCase = Depends(Provide(Container.lobby_history_use_case)),
        user_info: dict = Depends(verify_token)
):
    return await use_case.execute(user_info['email'])
