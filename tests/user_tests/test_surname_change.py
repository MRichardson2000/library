from data.classes.user import User
from data.database.queries.user_queries import UserQueries
from data.database.dbconn import execute_query
from data.dataclasses.db_dataclass import DB
from tests.auto_clear_db import auto_clear_user_table
from tests.auto_create_user import auto_create_user
from src.services.user_services import UserServices


def test_new_surname(user: User, db_session: DB) -> None:
    auto_clear_user_table()
    auto_create_user()
    output_before = execute_query("select * from users where first_name = 'user'")
    assert output_before is not None
    queries = UserQueries(db_session)
    service = UserServices(user, queries)
    service.change_surname("test")
    output_after = execute_query("select * from users where first_name = 'user'")
    assert output_after is not None
    assert output_after[0]["last_name"] == "test"
    assert user.last_name == "test"
    assert output_before[0]["last_name"] != output_after[0]["last_name"]
    auto_clear_user_table()
