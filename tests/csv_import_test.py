from unittest.mock import patch, MagicMock
import pytest
from fastapi import UploadFile
from io import BytesIO

from src.domain.redis_connector.redis_handler import RedisHandler
from src.usecase.csv_import import CsvImportUseCase
from src.contract.model import Story, Ticket

class MockRedisHandler(MagicMock, RedisHandler):
    pass

@pytest.mark.asyncio
async def test_execute():
    mock_redis_handler = MockRedisHandler()

    use_case = CsvImportUseCase(redis_handler=mock_redis_handler)

    csv_content = """Typ zgłoszenia,Id. zgłoszenia,Podsumowanie,Głosy,Parent summary
Story,1,Story One,10,
Podzadanie,2,Task One,5,Story One
Podzadanie,3,Task Two,8,Story One
Story,4,Story Two,15,
Podzadanie,5,Task Three,3,Story Two
"""

    upload_file = UploadFile(filename="test.csv", file=BytesIO(csv_content.encode()))

    with patch.object(upload_file, "read", return_value=csv_content.encode()):
        with patch.object(mock_redis_handler, "add_user_story", return_value=None) as mock_add_user_story:
            await use_case.execute(lobby_key="test_lobby_key", file=upload_file)

            expected_stories = {
                "Story One": Story(story_id="1", story_name="Story One", story_points=10, tickets=[
                    Ticket(ticket_name="Task One"),
                    Ticket(ticket_name="Task Two")
                ]),
                "Story Two": Story(story_id="4", story_name="Story Two", story_points=15, tickets=[
                    Ticket(ticket_name="Task Three")
                ])
            }

            for story in expected_stories.values():
                mock_add_user_story.assert_any_call("test_lobby_key", story.model_dump())

@pytest.mark.asyncio
async def test_execute_with_empty_file():
    mock_redis_handler = MockRedisHandler()
    use_case = CsvImportUseCase(redis_handler=mock_redis_handler)

    empty_csv_content = ""

    upload_file = UploadFile(filename="empty.csv", file=BytesIO(empty_csv_content.encode()))

    with patch.object(upload_file, "read", return_value=empty_csv_content.encode()):
        with patch.object(mock_redis_handler, "add_user_story", return_value=None) as mock_add_user_story:
            await use_case.execute(lobby_key="test_lobby_key", file=upload_file)

            mock_add_user_story.assert_not_called()

@pytest.mark.asyncio
async def test_execute_with_missing_story():
    mock_redis_handler = MockRedisHandler()
    use_case = CsvImportUseCase(redis_handler=mock_redis_handler)

    csv_content = """Typ zgłoszenia,Id. zgłoszenia,Podsumowanie,Głosy,Parent summary
Podzadanie,2,Task One,5,Story One
"""

    upload_file = UploadFile(filename="missing_story.csv", file=BytesIO(csv_content.encode()))

    with patch.object(upload_file, "read", return_value=csv_content.encode()):
        with patch.object(mock_redis_handler, "add_user_story", return_value=None) as mock_add_user_story:
            await use_case.execute(lobby_key="test_lobby_key", file=upload_file)

            mock_add_user_story.assert_not_called()
