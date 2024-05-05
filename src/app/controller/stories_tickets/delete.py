from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter

from src.app.container import Container
from src.app.request.delete_story import DeleteStoryRequest
from src.usecase.stories_tickets.delete_story import DeleteStoryUseCase

api = APIRouter()


@api.delete("/delete")
@inject
async def delete_story(
        request: DeleteStoryRequest,
        use_case: DeleteStoryUseCase = Depends(Provide(Container.delete_story_use_case))
) -> None:
    await use_case.execute(
        lobby_id=request.lobby_id,
        story_id=request.story_id
    )
