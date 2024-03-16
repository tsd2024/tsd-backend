from fastapi import APIRouter
from src.app.controller.dummy import router as dummy_router


def _v1() -> APIRouter:
    api = APIRouter(prefix='/v1')
    api.include_router(dummy_router)
    return api


def root_router() -> APIRouter:
    api = APIRouter(prefix='/api')
    api.include_router(_v1())
    return api
