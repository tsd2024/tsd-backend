import os

import pytest

from src.database.database import Database


@pytest.fixture()
def session_factory():
    db = Database(os.environ['DATABASE_URL'])
    db.remove_database()
    db.create_database()
    yield db.session
    db.remove_database()
