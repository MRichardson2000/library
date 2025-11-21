import pytest
from data.dbconn import load_env
from data.dataclasses import DB


@pytest.fixture
def db_session() -> DB:
    db = load_env(testing=True)
    return db
