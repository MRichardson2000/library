from __future__ import annotations
from data.classes.enums import AccountState
from data.database.queries.user_queries import UserQueries
from data.classes.user import User
from src.services.exceptions import (
    DatabaseServiceError,
)
import logging


class UserServices:
    def __init__(self, user: User, user_queries: UserQueries) -> None:
        self.user_queries = user_queries
        self.user = user

    def create_user(self) -> None:
        logging.info("Attempting to create user")
        try:
            self.user_queries.insert_user(self.user)
            logging.info("Successfully created user")
        except Exception as e:
            logging.exception("Failed to create user")
            raise DatabaseServiceError("Failed to create user") from e

    def get_user_details(self) -> User | None:
        logging.info("Attempting to get user details from the database")
        try:
            rows = self.user_queries.find_user(self.user.email_address)
            if rows:
                logging.info("Successfully retrieved user details")
                return rows
        except Exception as e:
            logging.exception("Failed to get user details from the database")
            raise DatabaseServiceError(
                "Failed to get user details from the database"
            ) from e

    def change_surname(self, new_surname: str) -> None:
        logging.info("Attempting to change surname for %s", self.user.first_name)
        self.user.last_name = new_surname
        try:
            self.user_queries.set_surname(self.user)
            logging.info("Successfully changed surname for %s", self.user.first_name)
        except Exception as e:
            logging.exception("Failed to change surname for %s", self.user.first_name)
            raise DatabaseServiceError(
                "Failed to change surname for %s", self.user.first_name
            ) from e

    def email_change(self, new_email_address: str) -> None:
        logging.info(
            "Attempting to change email address for %s %s",
            self.user.first_name,
            self.user.last_name,
        )
        self.user.email_address = new_email_address
        try:
            self.user_queries.set_email(self.user)
            logging.info(
                "Successfully changed email address for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
        except Exception as e:
            logging.exception(
                "Failed to change email address for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
            raise DatabaseServiceError(
                "Failed to change email address for %s %s",
                self.user.first_name,
                self.user.last_name,
            ) from e

    def phone_number_change(self, new_phone_number: str) -> None:
        logging.info(
            "Attempting to update phone number for %s %s",
            self.user.first_name,
            self.user.last_name,
        )
        self.user.phone_number = new_phone_number
        try:
            self.user_queries.set_phone_number(self.user)
            logging.info(
                "Successfully changed phone number for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
        except Exception as e:
            logging.exception(
                "Failed to change phone number for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
            raise DatabaseServiceError(
                "Failed to change phone_number for %s %s",
                self.user.first_name,
                self.user.last_name,
            ) from e

    def delete_user(self) -> None:
        logging.info(
            "Attempting to mark %s %s as deleted in the database",
            self.user.first_name,
            self.user.last_name,
        )
        self.user.account_state = AccountState.DELETED
        try:
            self.user_queries.set_status(self.user)
            logging.info(
                "Successfully changed the status to deleted for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
        except Exception as e:
            logging.exception(
                "Failed to change account_state to deleted for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
            raise DatabaseServiceError(
                "Failed to change account_state to deleted for %s %s",
                self.user.first_name,
                self.user.last_name,
            ) from e

    def restore_user(self) -> None:
        logging.info(
            "Attempting to mark %s %s as Active in the database",
            self.user.first_name,
            self.user.last_name,
        )
        self.user.account_state = AccountState.ACTIVE
        try:
            self.user_queries.set_status(self.user)
            logging.info(
                "Successfully marked %s %s as Active in the database",
                self.user.first_name,
                self.user.last_name,
            )
        except Exception as e:
            logging.exception(
                "Failed to change account_state to active for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
            raise DatabaseServiceError(
                "Failed to change account_state to active for %s %s",
                self.user.first_name,
                self.user.last_name,
            ) from e
