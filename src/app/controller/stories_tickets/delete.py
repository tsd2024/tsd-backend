from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException

from src.app.container import Container
from src.app.request.delete_story import DeleteStoryRequest
from src.contract.exceptions import UserStoryNotFoundException, LobbyNotFoundException
from src.domain.google_auth.token_verifier_request import verify_token
from src.usecase.stories_tickets.delete_story import DeleteStoryUseCase

api = APIRouter()


@api.delete(
    "/delete",
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
async def delete_story(
        request: DeleteStoryRequest,
        use_case: DeleteStoryUseCase = Depends(Provide(Container.delete_story_use_case)),
        user_info: dict = Depends(verify_token)
) -> None:
    try:
        await use_case.execute(
            lobby_id=request.lobby_id,
            story_id=request.story_id
        )
    except UserStoryNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LobbyNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

