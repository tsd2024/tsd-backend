from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from dependency_injector.wiring import Provide, inject
from src.app.container import Container
from src.contract.exceptions import LobbyNotFoundException
from src.domain.redis_connector.redis_handler import RedisHandler
from src.usecase.csv_export.export_csv_file import ExportCsvFile

api = APIRouter()

@api.get("/download_csv/{lobby_id}",
         responses=
         {
             404: {
                 "description": "Lobby not found"
             }
         }
         )
@inject
async def download_csv(lobby_id: str, redis_handler: RedisHandler = Depends(Provide(Container.redis_handler)), use_case: ExportCsvFile = Depends(Provide(Container.export_csv_file))) -> FileResponse:
    try:
        file = use_case.export(lobby_id, redis_handler)

        return FileResponse(file)
    
    except LobbyNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
