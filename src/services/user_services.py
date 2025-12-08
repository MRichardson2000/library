from __future__ import annotations
from data.dataclasses.db_dataclass import DB
from data.database.sql_models import users_insert
from data.classes.user import User
from src.services.base_services import DefaultFilterBuilder, QueryExecutor
from src.services.exceptions import (
    UserAlreadyExistsError,
    DatabaseServiceError,
    UserNotFoundError,
)
from typing import Any


class UserServices:
    def __init__(self, user: User, db: DB) -> None:
        self.filters = DefaultFilterBuilder(db)
        self.executor = QueryExecutor(db)
        self.user = user
        self.db = db

    def create_user(self) -> None:
        """
        Create user in the database if they don't already exist

        Raises:
            UserAlreadyExistsError: If user is found.
            DatabaseServiceError: If a database operation fails.
        """
        conditions, values = self.filters.build_conditions(self.user.filters())
        query = f"select * from users where {conditions}"
        try:
            user_check = self.executor.execute(query, values)
            if user_check:
                raise UserAlreadyExistsError("User already exists")
            self.executor.execute(users_insert, values)
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
        conditions, values = self.filters.build_conditions(self.user.filters())
        query = f"select * from users where {conditions}"
        try:
            get_user = self.executor.execute(query, values)
            if not get_user:
                raise UserNotFoundError("User not found in the database")
            return get_user
        except Exception as e:
            raise DatabaseServiceError("Failed to retrieve user details") from e

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
        conditions, values = self.filters.build_conditions(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        self.user.last_name = new_surname
        try:
            rows = self.executor.execute(find_user_query, values)
            if not rows:
                raise UserNotFoundError("Unable to find user, surname change aborted")
            if len(rows) > 1:
                raise ValueError(
                    "Modification aborted due to multiple rows being detected"
                )
            update_query = f"""
                            update user
                            set last_name = :last_name
                            where {conditions}
                            """
            values["last_name"] = self.user.last_name
            self.executor.execute(update_query, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to change users surname") from e

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
        conditions, values = self.filters.build_conditions(
            {"user_id": self.user.user_id}
        )
        find_user_query = f"select * from users where {conditions}"
        try:
            user_check = self.executor.execute(find_user_query, values)
            if not user_check:
                raise UserNotFoundError("Unable to find user, email change aborted")
            if len(user_check) > 1:
                raise ValueError(
                    "Modification aborted due to multiple rows being detected"
                )
            update_query = f"""
                            update users
                            set email_address = :new_email
                            where {conditions}
                            returning user_id;
                            """
            values["new_email"] = new_email_address
            rows = self.executor.execute(update_query, values)
            if not rows or "user_id" not in rows[0]:
                raise DatabaseServiceError("Modification did not find a user_id")
            self.user.user_id = rows[0]["user_id"]
            self.user.email_address = new_email_address
        except Exception as e:
            raise DatabaseServiceError("Failed to change email address") from e

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
        conditions, values = self.filters.build_conditions(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        self.user.phone_number = new_phone_number
        try:
            rows = self.executor.execute(find_user_query, values)
            if not rows:
                raise UserNotFoundError(
                    "Unable to find user, phone number change aborted"
                )
            if len(rows) > 1:
                raise ValueError(
                    "Modification aborted due to multiple rows being detected"
                )
            update_query = f"""
                            update user
                            set phone_number = :phone_number
                            where {conditions}
                            """
            values["last_name"] = self.user.last_name
            self.executor.execute(update_query, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to change phone number") from e

    def delete_user(self) -> None:
        """
        Mark the current user as deleted for audit purposes.

        Raises:
            UserNotFoundError: If the user is not found.
            DatabaseServiceError: If a database operation fails.
        """
        conditions, values = self.filters.build_conditions(self.user.filters())
        verification_query = f"select * from users where {conditions}"
        try:
            rows = self.executor.execute(verification_query, values)
            if not rows:
                raise UserNotFoundError("User not found, deletion aborted")
            if len(rows) > 1:
                raise ValueError("Deletion aborted due to multiple rows being found")
            delete_query = f"""
                            update user
                            set deleted = True
                            where {conditions}
                            """
            self.executor.execute(delete_query, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to delete user") from e
