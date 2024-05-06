import csv
from typing import List
from fastapi import UploadFile
from src.contract.model import Story, Ticket


class CsvImportUseCase:
    async def execute(self, file: UploadFile) -> List[Story]:
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

        return list(stories.values())