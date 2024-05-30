from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, UploadFile, File, Depends

from src.app.container import Container
from src.usecase.csv_import import CsvImportUseCase

api = APIRouter()


@api.post("/uploadcsv")
@inject
async def upload_csv(
        file: UploadFile = File(...),
        lobby_key: str = None,
        use_case: CsvImportUseCase = Depends(Provide(Container.csv_import_use_case))
):
    return await use_case.execute(lobby_key, file)
