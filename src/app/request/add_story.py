from pydantic import BaseModel

from src.contract.model import Ticket


class AddStoryRequest(BaseModel):
    story_name: str
    story_description: str
    tickets: list[Ticket]