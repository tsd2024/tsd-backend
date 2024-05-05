from pydantic import BaseModel

from src.contract.model import Ticket


class AddStoryRequest(BaseModel):
    lobby_id: str
    story_name: str
    tickets: list[Ticket]
