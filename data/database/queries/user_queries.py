from data.database.queries.base_queries import Queries
from data.database.sql_models import users_insert
from data.database.dbconn import fetch_result, execute_query
from typing import Any


class UserQueries(Queries):
    def find_by_first_name(self) -> list[dict[str, Any]] | None:
        rows = fetch_result(
            "select * from user where first_name = :first_name",
            {"first_name": self.user.first_name},
        )
        if rows:
            return rows

    def insert_user(self) -> None:
        execute_query(users_insert, self.user.to_dict())

    def set_surname(self) -> None:
        row = self.find_by_first_name()
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

    def set_email(self) -> None:
        row = self.find_by_first_name()
        if row:
            execute_query(
                """
                update users
                set email_address = :email_address
                where first_name = :first_name
                and user_id = :user_id
                """,
                {
                    "email_address": self.user.email_address,
                    "first_name": self.user.first_name,
                    "user_id": self.user.user_id,
                },
            )

    def set_phone_number(self) -> None:
        row = self.find_by_first_name()
        if row:
            execute_query(
                """
                update users
                set phone_number = :phone_number
                where first_name = :first_name
                and user_id = :user_id
                """,
                {
                    "phone_number": self.user.phone_number,
                    "first_name": self.user.first_name,
                    "user_id": self.user.user_id,
                },
            )

    def set_status(self) -> None:
        row = self.find_by_first_name()
        if row:
            execute_query(
                """
                update users
                set account_state = :account_state
                where first_name = :first_name
                and user_id = :user_id
                """,
                {
                    "account_state": self.user.account_state,
                    "first_name": self.user.first_name,
                    "user_id": self.user.user_id,
                },
            )
