from pydantic import BaseModel

from src.contract.model import Story
from src.domain.redis_connector.record import get_user_story_template
from src.domain.redis_connector.redis_handler import RedisHandler


class UpdateStoryUseCase(BaseModel):
    redis_handler: RedisHandler

    class Config:
        arbitrary_types_allowed = True

    async def execute(self, lobby_id: str, story: Story) -> None:
        template = get_user_story_template()
        template['story_id'] = story.story_id
        template['story_name'] = story.story_name
        template['story_points'] = story.story_points
        tickets = story.tickets
        for ticket in tickets:
            template['tickets'].append({
                'ticket_name': ticket.ticket_name
            })
        self.redis_handler.update_user_story(lobby_id, template)
