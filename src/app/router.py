from fastapi import APIRouter
from src.app.controller.dummy import router as dummy_router
from src.app.controller.websocket import api as websocket_api
from src.app.controller.create_lobby import api as create_lobby_api
from src.app.controller.google_auth import api as google_auth_api


def _v1() -> APIRouter:
    api = APIRouter(prefix='/v1')
    api.include_router(dummy_router)
    api.include_router(websocket_api)
    api.include_router(create_lobby_api)
    api.include_router(google_auth_api)
    return api


def root_router() -> APIRouter:
    api = APIRouter(prefix='/api')
    api.include_router(_v1())
    return api
