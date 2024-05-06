from dependency_injector.wiring import inject
from fastapi import APIRouter, UploadFile, File
from src.usecase.csv_import import CsvImportUseCase

api = APIRouter()


@api.post("/uploadcsv")
@inject
async def upload_csv(file: UploadFile = File(...)):
    return await CsvImportUseCase().execute(file)
