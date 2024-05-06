from src.domain.redis_connector.redis_handler import RedisHandler
import csv
import uuid
import os

class ExportCsvFile:

    def __init__(self, redis_handler: RedisHandler):
        self.redis_handler = redis_handler
    def export(self, lobby_id: str, redis_handler: RedisHandler):
        lobby_status = redis_handler.get_lobby_status(lobby_id)
        user_stories = lobby_status.get('user_stories', [])

        file_name = f'{lobby_id}.csv'
        file_path = os.path.join('csvfiles', file_name)
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Summary', 'Issue id', 'Issue Type', 'Custom field (Story point estimate)',
                             'Parent'])

            for story in user_stories:
                story_name = story.get('story_name', '')
                story_id = story.get('story_id', '')

                writer.writerow([story_name, story_id, 'Story', story.get('story_points', ''), ''])

                for ticket in story.get('tickets', []):
                    ticket_name = ticket.get('ticket_name', '')
                    ticket_id = str(uuid.uuid4())
                    writer.writerow([ticket_name, ticket_id, 'Pozadanie', '', story_name])
        return file_path