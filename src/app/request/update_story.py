from pydantic import BaseModel

from src.contract.model import Ticket


class UpdateStoryRequest(BaseModel):
    lobby_id: str
    story_id: str
    story_name: str
    tickets: list[Ticket]
