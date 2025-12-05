import pytest
from data.database.dbconn import load_env
from data.dataclasses.db_dataclass import DB


@pytest.fixture
def db_session() -> DB:
    db = load_env(testing=True)
    return db
