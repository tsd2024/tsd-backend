from fastapi import WebSocket
from dependency_injector.wiring import inject
from src.domain.google_auth.token_verifier_websocket import verify_token


@inject
def google_token_validation(websocket: WebSocket):
    token_info = verify_token(websocket)
    return token_info
