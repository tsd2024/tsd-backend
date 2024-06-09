import csv
import os
from unittest.mock import MagicMock

import pytest

from src.domain.redis_connector.redis_handler import RedisHandler
from src.usecase.csv_export.export_csv_file import ExportCsvFile


class MockRedisHandler(MagicMock, RedisHandler):
    pass


from unittest.mock import patch


@pytest.fixture
def mock_redis_handler():
    return MockRedisHandler()


def test_export_csv_file_with_no_user_stories(mock_redis_handler):
    mock_lobby_id = "lobby123"

    with patch.object(mock_redis_handler, "get_lobby_status") as mock_get_lobby_status:
        mock_get_lobby_status.return_value = {'user_stories': []}
        export_csv_file = ExportCsvFile(mock_redis_handler)
        file_path = export_csv_file.export(mock_lobby_id, mock_redis_handler)

        assert os.path.exists(file_path)

        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)

            assert rows[0] == ['Summary', 'Issue id', 'Issue Type', 'Custom field (Story point estimate)', 'Parent']
            assert len(rows) == 1
