from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter

from src.app.container import Container
from src.app.request.add_story import AddStoryRequest
from src.app.request.create_lobby import CreateLobbyRequest
from src.app.response.create_lobby import CreateLobbyResponse
from src.usecase.create_lobby import CreateLobbyUseCase
from src.usecase.stories_tickets.add_story import AddStoryUseCase

api = APIRouter()

@api.post("/add")
@inject
async def add_story(
        request: AddStoryRequest,
        use_case: AddStoryUseCase = Depends(Provide(Container.add_stories_use_case))
) -> None:

    await use_case.execute(
        lobby_id=request.admin_id,
        story=None
    )


