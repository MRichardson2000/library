import pytest
from data.database.dbconn import load_env
from data.dataclasses.db_dataclass import DB


@pytest.fixture(scope="function")
def db_session() -> DB:
    return load_env(testing=True)
