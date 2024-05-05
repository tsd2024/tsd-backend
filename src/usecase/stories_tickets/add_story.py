from pydantic import BaseModel

from src.contract.model import Story
from src.domain.redis_connector.redis_handler import RedisHandler


class AddStoryUseCase(BaseModel):
    redis_handler: RedisHandler

    class Config:
        arbitrary_types_allowed = True

    async def execute(self, lobby_id: str, story: Story) -> None:
        pass
