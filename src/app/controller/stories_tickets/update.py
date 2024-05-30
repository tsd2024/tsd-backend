from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException

from src.app.container import Container
from src.app.request.update_story import UpdateStoryRequest
from src.contract.exceptions import UserStoryNotFoundException, LobbyNotFoundException
from src.contract.model import Story
from src.domain.google_auth.token_verifier_request import verify_token
from src.usecase.stories_tickets.update_story import UpdateStoryUseCase

api = APIRouter()


@api.post(
    "/update",
    responses=
    {
        404: {
            "description": "Lobby not found"
        },
        400: {
            "description": "User story not found"
        }
    }
)
@inject
async def update_story(
        request: UpdateStoryRequest,
        use_case: UpdateStoryUseCase = Depends(Provide(Container.update_story_use_case)),
        user_info: dict = Depends(verify_token)
) -> None:
    story = Story(
        story_id=request.story_id,
        story_name=request.story_name,
        story_points=0,
        tickets=request.tickets
    )
    try:
        await use_case.execute(
            lobby_id=request.lobby_id,
            story=story
        )
    except UserStoryNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LobbyNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
