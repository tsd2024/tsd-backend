from fastapi import APIRouter

router = APIRouter()


@router.get('/dummy')
async def dummy():
    return {'dummy': 'dummy'}