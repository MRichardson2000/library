from data.classes.user import User
from data.database.dbconn import execute_query
from data.dataclasses.db_dataclass import DB
from tests.auto_clear_db import auto_clear_user_table
from src.services.user_services import UserServices


def test_new_surname(db_session: DB) -> None:
    auto_clear_user_table()
    user = User(
        None,
        first_name="user",
        last_name="user",
        email_address="user@user.user.user",
        phone_number="07384904391",
    )
    service = UserServices(user, db_session)
    service.create_user()
    output_before = execute_query(
        "select * from users where first_name = 'user'", db_details=db_session
    )
    assert output_before is not None
    service.change_surname("test")
    output_after = execute_query(
        "select * from users where first_name = 'user'", db_details=db_session
    )
    assert output_after is not None
    assert output_after[0]["last_name"] == "test"
    assert user.last_name == "test"
    assert output_before[0]["last_name"] != output_after[0]["last_name"]
    auto_clear_user_table()
