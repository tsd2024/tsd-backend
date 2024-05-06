import csv

from fastapi import UploadFile
from pydantic import BaseModel

from src.contract.model import Story, Ticket
from src.domain.redis_connector.redis_handler import RedisHandler


class CsvImportUseCase(BaseModel):
    redis_handler: RedisHandler

    class Config:
        arbitrary_types_allowed = True

    async def execute(self, lobby_key: str, file: UploadFile) -> None:
        file_content = await file.read()
        rows = list(csv.DictReader(file_content.decode().splitlines()))

        stories = {}
        for row in rows:
            if row['Typ zgłoszenia'] == 'Story':
                stories[row['Podsumowanie']] = Story(story_id=row['Id. zgłoszenia'], story_name=row['Podsumowanie'],
                                                     story_points=int(row['Głosy']), tickets=[])

        for row in rows:
            if row['Typ zgłoszenia'] == 'Podzadanie':
                ticket = Ticket(ticket_name=row['Podsumowanie'])
                parent_story = stories.get(row['Parent summary'])
                if parent_story:
                    parent_story.tickets.append(ticket)

        for story in stories.values():
            try:
                self.redis_handler.add_user_story(lobby_key, story.dict())
            except Exception as e:
                break
