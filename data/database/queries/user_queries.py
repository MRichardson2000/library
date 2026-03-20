from data.database.sql_models import users_insert
from data.classes.user import User
from data.database.dbconn import fetch_result, execute_query


class UserQueries:
    def __init__(self) -> None:
        pass

    def find_user(self, email_address: str) -> User | None:
        rows = fetch_result(
            "select * from user where email_address = :email_address",
            {"email_address": email_address},
        )
        return User.from_db_row(rows[0]) if rows else None

    def insert_user(self, user: User) -> None:
        row = self.find_user(user.email_address)
        if not row:
            execute_query(users_insert, user.to_dict())

    def set_surname(self, user: User) -> None:
        row = self.find_user(user.email_address)
        if row:
            execute_query(
                """
                update users
                set last_name = :last_name
                where first_name = :first_name
                and user_id = :user_id
                """,
                {"last_name": self},
            )

    def set_email(self, user: User) -> None:
        row = self.find_user(user.email_address)
        if row:
            execute_query(
                """
                update users
                set email_address = :email_address
                where first_name = :first_name
                and user_id = :user_id
                """,
                {
                    "email_address": user.email_address,
                    "first_name": user.first_name,
                    "user_id": user.user_id,
                },
            )

    def set_phone_number(self, user: User) -> None:
        row = self.find_user(user.email_address)
        if row:
            execute_query(
                """
                update users
                set phone_number = :phone_number
                where first_name = :first_name
                and user_id = :user_id
                """,
                {
                    "phone_number": user.phone_number,
                    "first_name": user.first_name,
                    "user_id": user.user_id,
                },
            )

    def set_status(self, user: User) -> None:
        row = self.find_user(user.email_address)
        if row:
            execute_query(
                """
                update users
                set account_state = :account_state
                where first_name = :first_name
                and user_id = :user_id
                """,
                {
                    "account_state": user.account_state,
                    "first_name": user.first_name,
                    "user_id": user.user_id,
                },
            )
