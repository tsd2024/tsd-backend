from dependency_injector.wiring import inject
from fastapi import Depends, APIRouter

from src.domain.google_auth.token_verifier_request import verify_token

api = APIRouter()


@api.get("/secure-route")
@inject
async def secure_route(user_info: dict = Depends(verify_token)):
    return {"message": "This is a secure route", "user": user_info}
