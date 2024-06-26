from fastapi import APIRouter
from src.app.controller.dummy import router as dummy_router
from src.app.controller.websocket import api as websocket_api
from src.app.controller.create_lobby import api as create_lobby_api
from src.app.controller.lobby_history import api as lobby_history_api

from src.app.controller.google_auth import api as google_auth_api

from src.app.controller.stories_tickets.add import api as add_stories_tickets_api
from src.app.controller.stories_tickets.update import api as update_stories_tickets_api
from src.app.controller.stories_tickets.delete import api as delete_stories_tickets_api
from src.app.controller.csv_file_export import api as csv_file_export_api


from src.app.controller.csv_import import api as csv_import_api


def user_story_router() -> APIRouter:
    api = APIRouter(prefix='/story')
    api.include_router(add_stories_tickets_api)
    api.include_router(update_stories_tickets_api)
    api.include_router(delete_stories_tickets_api)
    api.include_router(csv_file_export_api)
    return api

def _v1() -> APIRouter:
    api = APIRouter(prefix='/v1')
    api.include_router(dummy_router)
    api.include_router(websocket_api)
    api.include_router(create_lobby_api)
    api.include_router(google_auth_api)
    api.include_router(user_story_router())
    api.include_router(csv_import_api)
    api.include_router(lobby_history_api)
    return api


def root_router() -> APIRouter:
    api = APIRouter(prefix='/api')
    api.include_router(_v1())
    return api
