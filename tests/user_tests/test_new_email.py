from data.database.dbconn import execute_query
from data.dataclasses.db_dataclass import DB
from data.classes.user import User
from data.database.queries.user_queries import UserQueries
from src.services.user_services import UserServices
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_user import auto_create_user


def test_new_email(user: User, db_session: DB) -> None:
    auto_clear_table("users", db_session)
    auto_create_user(db_session)
    output_before = execute_query("select * from users where first_name = 'user'")
    assert output_before is not None
    queries = UserQueries(db_session)
    service = UserServices(user, queries)
    service.email_change("user1@user.user.user")
    output_after = execute_query("select * from users where first_name = 'user'")
    assert output_after is not None
    assert output_after[0]["email_address"] == "user1@user.user.user"
    assert user.email_address == "user1@user.user.user"
    assert output_before[0]["email_address"] != output_after[0]["email_address"]
    auto_clear_table("users", db_session)
