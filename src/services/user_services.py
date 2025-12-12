from __future__ import annotations
from data.database.query import FIND_BY_FIRST_NAME
from data.classes.enums import AccountState
from data.database.dbconn import execute_query, fetch_result
from data.database.sql_models import users_insert
from data.classes.user import User
from src.services.exceptions import (
    DatabaseServiceError,
    UserNotFoundError,
)
from typing import Any


class UserServices:
    def __init__(self, user: User) -> None:
        self.user = user

    def create_user(self) -> None:
        """
        Create user in the database if they don't already exist

        Raises:
            UserAlreadyExistsError: If user is found.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_FIRST_NAME, {"first_name": self.user.first_name})
            if not row:
                raise UserNotFoundError()
            execute_query(users_insert, self.user.to_dict())
        except Exception as e:
            raise DatabaseServiceError("Failed to create user") from e

    def get_user_details(self) -> list[dict[str, Any]]:
        """
        Retrieve details of the current user from the database if they exist.

        Returns:
            list[dict[str, Any]]: A list of matching user records.

        Raises:
            UserNotFoundError: If no user is found.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_FIRST_NAME, {"first_name": self.user.first_name})
            if not row:
                raise UserNotFoundError()
            return row
        except Exception as e:
            raise DatabaseServiceError("Failed to get user details") from e

    def change_surname(self, new_surname: str) -> None:
        """
        Update the surname of the current user in the database.

        Args:
            new_surname (str): The new surname value.

        Raises:
            UserNotFoundError: If no user is found.
            ValueError: If multiple matches exist.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_FIRST_NAME, {"first_name": self.user.first_name})
            if not row:
                raise UserNotFoundError()
            self.user.last_name = new_surname
            user_id = row[0]

            execute_query(
                "update users set last_name = :last_name where first_name = :first_name and user_id = :user_id",
                {
                    "last_name": self.user.last_name,
                    "first_name": self.user.first_name,
                    "user_id": user_id,
                },
            )
        except Exception as e:
            raise DatabaseServiceError("Failed to change surname") from e

    def email_change(self, new_email_address: str) -> None:
        """
        Update the email address of the current user in the database.

        Args:
            new_email_address (str): The new email address.

        Raises:
            UserNotFoundError: If no user is found.
            ValueError: If multiple matches exist.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_FIRST_NAME, {"first_name": self.user.first_name})
            if not row:
                raise UserNotFoundError()
            self.user.email_address = new_email_address
            user_id = row[0]
            execute_query(
                "update users set email_address = :email_address where first_name = :first_name and user_id = :user_id",
                {
                    "email_address": self.user.email_address,
                    "first_name": self.user.first_name,
                    "user_id": user_id,
                },
            )
        except Exception as e:
            raise DatabaseServiceError("Failed to change email") from e

    def phone_number_change(self, new_phone_number: str) -> None:
        """
        Update the phone number of the current user in the database.

        Args:
            new_phone_number (str): The new phone number.

        Raises:
            UserNotFoundError: If no user is found.
            ValueError: If multiple matches exist.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_FIRST_NAME, {"first_name": self.user.first_name})
            if not row:
                raise UserNotFoundError()
            self.user.phone_number = new_phone_number
            user_id = row[0]
            execute_query(
                "update users set phone_number = :phone_number where first_name = :first_name and user_id = :user_id",
                {
                    "phone_number": self.user.phone_number,
                    "first_name": self.user.first_name,
                    "user_id": user_id,
                },
            )
        except Exception as e:
            raise DatabaseServiceError("Failed to change phone_number") from e

    def delete_user(self) -> None:
        """
        Mark the current user as deleted for audit purposes.

        Raises:
            UserNotFoundError: If the user is not found.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_FIRST_NAME, {"first_name": self.user.first_name})
            if not row:
                raise UserNotFoundError()
            self.user.account_state = AccountState.DELETED
            user_id = row[0]
            execute_query(
                "update users set account_state = :account_state where first_name = :first_name and user_id = :user_id",
                {
                    "account_state": self.user.account_state,
                    "first_name": self.user.first_name,
                    "user_id": user_id,
                },
            )
        except Exception as e:
            raise DatabaseServiceError(
                "Failed to change account_state to deleted"
            ) from e

    def restore_user(self) -> None:
        """
        Restore user from the database if they exist

        Raises:
            UserNotFoundError: If user is not found.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_FIRST_NAME, {"first_name": self.user.first_name})
            if not row:
                raise UserNotFoundError()
            self.user.account_state = AccountState.ACTIVE
            user_id = row[0]
            execute_query(
                "update users set account_state = :account_state where first_name = :first_name and user_id = :user_id",
                {
                    "account_state": self.user.account_state,
                    "first_name": self.user.first_name,
                    "user_id": user_id,
                },
            )
        except Exception as e:
            raise DatabaseServiceError(
                "Failed to change account_state to active"
            ) from e
