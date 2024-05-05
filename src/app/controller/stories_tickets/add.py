import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter

from src.app.container import Container
from src.app.request.add_story import AddStoryRequest
from src.contract.model import Story
from src.usecase.stories_tickets.add_story import AddStoryUseCase

api = APIRouter()


@api.post("/add")
@inject
async def add_story(
        request: AddStoryRequest,
        use_case: AddStoryUseCase = Depends(Provide(Container.add_stories_use_case))
) -> None:
    story = Story(
        story_id=str(uuid.uuid4()),
        story_name=request.story_name,
        story_points=0,
        tickets=request.tickets
    )
    await use_case.execute(
        lobby_id=request.lobby_id,
        story=story
    )
