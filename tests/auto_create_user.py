from data.classes.user import User
from src.services.user_services import UserServices
from src.services.base_services import UserQueryExecutor, DefaultFilterBuilder
from data.dataclasses.db_dataclass import DB
from data.database.dbconn import load_env


def auto_create_user(
    db_session: DB = load_env(testing=True),
) -> tuple[User, UserServices]:
    user = User(
        first_name="user",
        last_name="user",
        email_address="user@user.user.user",
        phone_number="0123456789",
    )
    executor = UserQueryExecutor(db_session)
    filters = DefaultFilterBuilder(db_session)
    service = UserServices(user, executor, filters)
    service.create_user()
    return user, service
