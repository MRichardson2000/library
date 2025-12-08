from __future__ import annotations
from data.database.sql_models import users_insert
from data.classes.user import User
from src.services.base_services import UserQueryExecutor, FilterBuilder
from src.services.exceptions import (
    UserAlreadyExistsError,
    DatabaseServiceError,
    UserNotFoundError,
)
import logging
from typing import Any


class UserServices:
    def __init__(
        self, user: User, executor: UserQueryExecutor, filters: FilterBuilder
    ) -> None:
        self.user = user
        self.executor = executor
        self.filters = filters

    def create_user(self) -> None:
        """
        Create user in the database if they don't already exist

        Raises:
            UserAlreadyExistsError: If user is found.
            DatabaseServiceError: If a database operation fails.
        """
        logging.info(
            "Attempting to create user: %s %s",
            self.user.first_name,
            self.user.last_name,
        )
        conditions, values = self.filters.build_conditions(self.user.filters())
        query = f"select * from users where {conditions}"
        try:
            user_check = self.executor.execute(query, values)
            if user_check:
                usr_msg = "User already exists"
                logging.warning(usr_msg)
                raise UserAlreadyExistsError(usr_msg)
            self.executor.execute(users_insert, values)
            logging.info(
                "User created successfully: %s %s",
                self.user.first_name,
                self.user.last_name,
            )
        except Exception as e:
            err_msg = "Failed to create user"
            logging.exception(err_msg)
            raise DatabaseServiceError(err_msg) from e

    def get_user_details(self) -> list[dict[str, Any]]:
        """
        Retrieve details of the current user from the database if they exist.

        Returns:
            list[dict[str, Any]]: A list of matching user records.

        Raises:
            UserNotFoundError: If no user is found.
            DatabaseServiceError: If a database operation fails.
        """
        logging.info(
            "Attempting to retrieve user details %s %s",
            self.user.first_name,
            self.user.last_name,
        )
        conditions, values = self.filters.build_conditions(self.user.filters())
        query = f"select * from users where {conditions}"
        try:
            get_user = self.executor.execute(query, values)
            if not get_user:
                usr_msg = "User not found in the database"
                logging.warning(usr_msg)
                raise UserNotFoundError(usr_msg)
            logging.info("User details retrieved sucessfully")
            return get_user
        except Exception as e:
            err_msg = "Failed to retrieve user details"
            logging.exception(err_msg)
            raise DatabaseServiceError(err_msg) from e

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
        logging.info(
            "Attempting to update surname for user %s %s",
            self.user.first_name,
            self.user.last_name,
        )
        conditions, values = self.filters.build_conditions(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        self.user.last_name = new_surname
        try:
            rows = self.executor.execute(find_user_query, values)
            if not rows:
                usr_msg = "Unable to find user, surname change aborted"
                logging.warning(usr_msg)
                raise UserNotFoundError(usr_msg)
            if len(rows) > 1:
                mulrow_msg = "Modification aborted due to multiple rows being detected"
                logging.warning(mulrow_msg)
                raise ValueError(mulrow_msg)
            update_query = f"""
                            update user
                            set last_name = :last_name
                            where {conditions}
                            """
            values["last_name"] = self.user.last_name
            self.executor.execute(update_query, values)
            logging.info("Surname updated successfully")
        except Exception as e:
            fail_msg = "Failed to change users surname"
            logging.exception(fail_msg)
            raise DatabaseServiceError(fail_msg) from e

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
        logging.info(
            "Attempting to update Email address for user %s %s",
            self.user.first_name,
            self.user.last_name,
        )
        conditions, values = self.filters.build_conditions(
            {"user_id": self.user.user_id}
        )
        find_user_query = f"select * from users where {conditions}"
        try:
            user_check = self.executor.execute(find_user_query, values)
            if not user_check:
                usr_msg = "Unable to find userd"
                logging.warning(usr_msg)
                raise UserNotFoundError(usr_msg)
            if len(user_check) > 1:
                mulrow_msg = "Modification aborted due to multiple rows being detected"
                logging.warning(mulrow_msg)
                raise ValueError(mulrow_msg)
            update_query = f"""
                            update users
                            set email_address = :new_email
                            where {conditions}
                            returning user_id;
                            """
            values["new_email"] = new_email_address
            rows = self.executor.execute(update_query, values)
            if not rows or "user_id" not in rows[0]:
                id_msg = "User ID not found"
                logging.warning(id_msg)
                raise DatabaseServiceError(id_msg)
            self.user.user_id = rows[0]["user_id"]
            self.user.email_address = new_email_address
            logging.info("Updated email address in the database successfully")
        except Exception as e:
            fail_msg = "Failed to change email address"
            logging.exception(fail_msg)
            raise DatabaseServiceError(fail_msg) from e

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
        logging.info("Attempting to update phone number")
        conditions, values = self.filters.build_conditions(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        self.user.phone_number = new_phone_number
        try:
            rows = self.executor.execute(find_user_query, values)
            if not rows:
                usr_msg = "Unable to find user"
                logging.warning(usr_msg)
                raise UserNotFoundError(usr_msg)
            if len(rows) > 1:
                mulrow_msg = "Modification aborted due to multiple rows being detected"
                logging.warning(mulrow_msg)
                raise ValueError(mulrow_msg)
            update_query = f"""
                            update user
                            set phone_number = :phone_number
                            where {conditions}
                            """
            values["last_name"] = self.user.last_name
            self.executor.execute(update_query, values)
            logging.info("Updated phone number successfully")
        except Exception as e:
            fail_msg = "Failed to change phone number"
            logging.exception(fail_msg)
            raise DatabaseServiceError(fail_msg) from e

    def delete_user(self) -> None:
        """
        Mark the current user as deleted for audit purposes.

        Raises:
            UserNotFoundError: If the user is not found.
            DatabaseServiceError: If a database operation fails.
        """
        logging.info("Attempting to Mark user as deleted in the database")
        conditions, values = self.filters.build_conditions(self.user.filters())
        verification_query = f"select * from users where {conditions}"
        try:
            rows = self.executor.execute(verification_query, values)
            if not rows:
                usr_msg = "User not found"
                logging.warning(usr_msg)
                raise UserNotFoundError(usr_msg)
            if len(rows) > 1:
                mulrow_msg = "Deletion aborted due to multiple rows being found"
                logging.warning(mulrow_msg)
                raise ValueError(mulrow_msg)
            delete_query = f"""
                            update user
                            set deleted = True
                            where {conditions}
                            """
            self.executor.execute(delete_query, values)
            logging.info("Marked user as deleted in the database successfully")
        except Exception as e:
            fail_msg = "Failed to delete user"
            logging.exception(fail_msg)
            raise DatabaseServiceError(fail_msg) from e
