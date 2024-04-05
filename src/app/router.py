from fastapi import APIRouter
from src.app.controller.dummy import router as dummy_router
from src.app.controller.google_validation import app as google_validation


def _v1() -> APIRouter:
    api = APIRouter(prefix='/v1')
    api.include_router(dummy_router)
    api.include_router(google_validation)
    return api


def root_router() -> APIRouter:
    api = APIRouter(prefix='/api')
    api.include_router(_v1())
    return api
