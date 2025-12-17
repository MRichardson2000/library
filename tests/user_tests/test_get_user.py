from tests.auto_create_user import auto_create_user
from data.database.dbconn import execute_query
from tests.auto_clear_db import auto_clear_user_table


def test_get_user() -> None:
    auto_clear_user_table()
    auto_create_user()
    output = execute_query("select * from users where first_name = 'user'")
    assert output is not None
    assert output[0]["first_name"] == "user"
    assert output[0]["last_name"] == "user"
    assert output[0]["email_address"] == "user@user.user.user"
    assert output[0]["phone_number"] == "0123456789"
    auto_clear_user_table()
