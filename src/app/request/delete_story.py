from pydantic import BaseModel


class DeleteStoryRequest(BaseModel):
    lobby_id: str
    story_id: str
