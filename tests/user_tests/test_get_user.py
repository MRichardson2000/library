from data.classes.user import User
from data.database.dbconn import execute_query
from data.dataclasses.db_dataclass import DB
from tests.auto_clear_db import auto_clear_user_table
from src.services.user_services import UserServices


def test_get_user(db_session: DB) -> None:
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
    output = execute_query(
        "select * from users where first_name = 'user'", db_details=db_session
    )
    assert output is not None
    assert output[0]["first_name"] == "user"
    assert output[0]["last_name"] == "user"
    assert output[0]["email_address"] == "user@user.user.user"
    assert output[0]["phone_number"] == "07384904391"
    auto_clear_user_table()
