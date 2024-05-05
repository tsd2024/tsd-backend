from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter

from src.app.container import Container
from src.app.request.update_story import UpdateStoryRequest
from src.contract.model import Story
from src.usecase.stories_tickets.update_story import UpdateStoryUseCase

api = APIRouter()


@api.post("/update")
@inject
async def update_story(
        request: UpdateStoryRequest,
        use_case: UpdateStoryUseCase = Depends(Provide(Container.update_story_use_case))
) -> None:
    story = Story(
        story_id=request.story_id,
        story_name=request.story_name,
        story_points=0,
        tickets=request.tickets
    )
    await use_case.execute(
        lobby_id=request.lobby_id,
        story=story
    )
