from pydantic import BaseModel


class CreateLobbyRequest(BaseModel):
    lobby_name: str
    max_players: int
    number_of_rounds: int
    admin_id: str

