from pydantic import BaseModel


class CreateLobbyResponse(BaseModel):
    lobby_id: str
    lobby_name: str
    admin_id: str