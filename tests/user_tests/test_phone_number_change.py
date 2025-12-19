from data.classes.user import User
from data.database.queries.user_queries import UserQueries
from data.database.dbconn import execute_query
from data.dataclasses.db_dataclass import DB
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_user import auto_create_user
from src.services.user_services import UserServices


def test_new_phone_number(user: User, db_session: DB) -> None:
    auto_clear_table("users", db_session)
    auto_create_user(db_session)
    output_before = execute_query("select * from users where first_name = 'user'")
    assert output_before is not None
    queries = UserQueries(db_session)
    service = UserServices(user, queries)
    service.phone_number_change("11111111111")
    output_after = execute_query("select * from users where first_name = 'user'")
    assert output_after is not None
    assert output_after[0]["phone_number"] == "11111111111"
    assert user.phone_number == "11111111111"
    assert output_before[0]["phone_number"] != output_after[0]["phone_number"]
    auto_clear_table("users", db_session)
