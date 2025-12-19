from data.classes.user import User
from data.database.queries.user_queries import UserQueries
from src.services.user_services import UserServices
from data.dataclasses.db_dataclass import DB


def auto_create_user(db_session: DB) -> User:
    user = User(
        first_name="user",
        last_name="user",
        email_address="user@user.user.user",
        phone_number="0123456789",
    )
    queries = UserQueries(db_session)
    service = UserServices(user, queries)
    service.create_user()
    return user
