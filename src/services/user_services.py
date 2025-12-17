from __future__ import annotations
from data.classes.enums import AccountState
from data.database.queries.user_queries import UserQueries
from data.classes.user import User
from src.services.exceptions import (
    DatabaseServiceError,
)
from typing import Any


class UserServices:
    def __init__(self, user: User, user_queries: UserQueries) -> None:
        self.user_queries = user_queries
        self.user = user

    def create_user(self) -> None:
        try:
            self.user_queries.insert_user(self.user)
        except Exception as e:
            raise DatabaseServiceError("Failed to create user") from e

    def get_user_details(self) -> dict[str, Any] | None:
        try:
            rows = self.user_queries.find_by_first_name(self.user)
            if rows:
                return rows[0]
        except Exception as e:
            raise DatabaseServiceError("Failed to get user details") from e

    def change_surname(self, new_surname: str) -> None:
        self.user.last_name = new_surname
        try:
            self.user_queries.set_surname(self.user)
        except Exception as e:
            raise DatabaseServiceError("Failed to change surname") from e

    def email_change(self, new_email_address: str) -> None:
        self.user.email_address = new_email_address
        try:
            self.user_queries.set_email(self.user)
        except Exception as e:
            raise DatabaseServiceError("Failed to change email") from e

    def phone_number_change(self, new_phone_number: str) -> None:
        self.user.phone_number = new_phone_number
        try:
            self.user_queries.set_phone_number(self.user)
        except Exception as e:
            raise DatabaseServiceError("Failed to change phone_number") from e

    def delete_user(self) -> None:
        self.user.account_state = AccountState.DELETED
        try:
            self.user_queries.set_status(self.user)
        except Exception as e:
            raise DatabaseServiceError(
                "Failed to change account_state to deleted"
            ) from e

    def restore_user(self) -> None:
        self.user.account_state = AccountState.ACTIVE
        try:
            self.user_queries.set_status(self.user)
        except Exception as e:
            raise DatabaseServiceError(
                "Failed to change account_state to active"
            ) from e
