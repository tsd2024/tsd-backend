import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException

from src.app.container import Container
from src.app.request.add_story import AddStoryRequest
from src.contract.exceptions import LobbyNotFoundException, MaxUserStoriesReachedException
from src.contract.model import Story
from src.usecase.stories_tickets.add_story import AddStoryUseCase

api = APIRouter()


@api.post(
    "/add",
    responses=
    {
        404: {
            "description": "Lobby not found"
        },
        400: {
            "description": "Max user stories reached"
        }
    }
)
@inject
async def add_story(
        request: AddStoryRequest,
        use_case: AddStoryUseCase = Depends(Provide(Container.add_story_use_case))
) -> None:
    story = Story(
        story_id=str(uuid.uuid4()),
        story_name=request.story_name,
        story_points=0,
        tickets=request.tickets
    )
    try:
        await use_case.execute(
            lobby_id=request.lobby_id,
            story=story
        )
    except LobbyNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MaxUserStoriesReachedException as e:
        raise HTTPException(status_code=400, detail=str(e))
