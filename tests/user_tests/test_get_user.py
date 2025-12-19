from tests.auto_create_user import auto_create_user
from data.database.dbconn import execute_query
from tests.auto_clear_db import auto_clear_table
from data.dataclasses.db_dataclass import DB


def test_get_user(db_session: DB) -> None:
    auto_clear_table("users", db_session)
    auto_create_user(db_session)
    output = execute_query("select * from users where first_name = 'user'")
    assert output is not None
    assert output[0]["first_name"] == "user"
    assert output[0]["last_name"] == "user"
    assert output[0]["email_address"] == "user@user.user.user"
    assert output[0]["phone_number"] == "0123456789"
    auto_clear_table("users", db_session)
