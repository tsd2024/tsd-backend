from pydantic import BaseModel

from src.contract.model import Story
from src.domain.redis_connector.record import get_user_story_template
from src.domain.redis_connector.redis_handler import RedisHandler


class DeleteStoryUseCase(BaseModel):
    redis_handler: RedisHandler

    class Config:
        arbitrary_types_allowed = True

    async def execute(self, lobby_id: str, story_id: str) -> None:
        self.redis_handler.delete_user_story(lobby_id, story_id)
