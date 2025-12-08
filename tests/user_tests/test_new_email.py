from data.database.dbconn import execute_query
from data.dataclasses.db_dataclass import DB
from tests.auto_clear_db import auto_clear_user_table
from tests.auto_create_user import auto_create_user


def test_new_email(db_session: DB) -> None:
    auto_clear_user_table()
    user, service = auto_create_user(db_session)
    output_before = execute_query(
        "select * from users where first_name = 'user'", db_details=db_session
    )
    assert output_before is not None
    service.email_change("user1@user.user.user")
    output_after = execute_query(
        "select * from users where first_name = 'user'", db_details=db_session
    )
    assert output_after is not None
    assert output_after[0]["email_address"] == "user1@user.user.user"
    assert user.email_address == "user1@user.user.user"
    assert output_before[0]["email_address"] != output_after[0]["email_address"]
    auto_clear_user_table()
