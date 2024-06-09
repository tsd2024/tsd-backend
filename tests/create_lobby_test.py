from unittest.mock import patch, MagicMock
import pytest
from src.contract.model import BasicLobbyInfo
from src.domain.redis_connector.record import get_redis_record_template
from src.domain.redis_connector.redis_handler import RedisHandler
from src.usecase.create_lobby import CreateLobbyUseCase


class MockRedisHandler(MagicMock, RedisHandler):
    pass


@pytest.mark.asyncio
async def test_execute():
    admin_id = "admin123"
    lobby_name = "Test Lobby"
    max_players = 10
    number_of_rounds = 5

    mock_lobby_key = "123-456"

    expected_result = BasicLobbyInfo(
        lobby_id=mock_lobby_key,
        lobby_name=lobby_name,
        admin_id=admin_id
    )

    # Create a mock redis_handler using the subclass
    mock_redis_handler = MockRedisHandler()

    # Initialize CreateLobbyUseCase with the mocked redis_handler
    use_case = CreateLobbyUseCase(redis_handler=mock_redis_handler)

    with patch("src.usecase.create_lobby.generate_unique_id", return_value=mock_lobby_key):
        with patch.object(mock_redis_handler, "upload_record", return_value=None) as mock_upload_record:
            result = await use_case.execute(admin_id, lobby_name, max_players, number_of_rounds)

            expected_value = get_redis_record_template()
            expected_value['lobby_metadata']['max_players'] = max_players
            expected_value['lobby_metadata']['number_of_rounds'] = number_of_rounds
            expected_value['lobby_metadata']['lobby_name'] = lobby_name
            expected_value['lobby_metadata']['admin_id'] = admin_id
            expected_value['players'][0]['player_id'] = admin_id

            mock_upload_record.assert_called_once_with(str(mock_lobby_key), expected_value)

            assert result == expected_result
