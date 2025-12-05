from __future__ import annotations
from data.database.dbconn import execute_query
from data.database.sql_models import users_insert
from data.database.orm_models import UserORM
from src.repositories.user_repository import UserRepository
from src.services.base_services import BaseService
from src.services.exceptions import (
    UserAlreadyExistsError,
    DatabaseServiceError,
    UserNotFoundError,
)
from typing import Any


class UserServices:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(
        self, first_name: str, last_name: str, email_address: str, phone_number: int
    ) -> UserORM:
        self.repository.assert_not_exists_by_email(email_address)

        new_user = UserORM(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
        )
        try:
            self.repository.insert(new_user)
        except Exception as e:
            raise DatabaseServiceError("Failed to create user") from e
        return new_user

    def get_user_details(self) -> list[dict[str, Any]]:
        """
        Retrieve details of the current user from the database.

        Returns:
            list[dict[str, Any]]: A list of matching user records.

        Raises:
            UserNotFoundError: If no user is found.
            DatabaseServiceError: If a database operation fails.
        """
        rows = self.repository.find_by_filters(self.user.filters())
        query = f"select * from users where {conditions}"
        try:
            get_user = execute_query(query, values)
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
        rows = self.repository.find_by_filters(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        self.user.last_name = new_surname
        try:
            rows = execute_query(find_user_query, values)
            if not rows:
                raise UserNotFoundError("Unable to find user, surname change aborted")
            if len(rows) > 1:
                raise ValueError(
                    "Modification aborted due to multiple rows being detected"
                )
            update_query = f"""
                            update user
                            set last_name = {self.user.last_name}
                            where {conditions}
                            """
            execute_query(update_query)
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
        rows = self.repository.find_by_filters(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        self.user.email_address = new_email_address
        try:
            rows = execute_query(find_user_query, values)
            if not rows:
                raise UserNotFoundError("Unable to find user, email change aborted")
            if len(rows) > 1:
                raise ValueError(
                    "Modification aborted due to multiple rows being detected"
                )
            update_query = f"""
                            update user
                            set email_address = {self.user.email_address}
                            where {conditions}
                            """
            execute_query(update_query)
        except Exception as e:
            raise DatabaseServiceError("Failed to change email address") from e

    def phone_number_change(self, new_phone_number: int) -> None:
        """
        Update the phone number of the current user in the database.

        Args:
            new_phone_number (str): The new phone number.

        Raises:
            UserNotFoundError: If no user is found.
            ValueError: If multiple matches exist.
            DatabaseServiceError: If a database operation fails.
        """
        rows = self.repository.find_by_filters(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        self.user.phone_number = new_phone_number
        try:
            rows = execute_query(find_user_query, values)
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
                            set phone_number = {self.user.phone_number}
                            where {conditions}
                            """
            execute_query(update_query)
        except Exception as e:
            raise DatabaseServiceError("Failed to change phone number") from e

    def delete_user(self) -> None:
        """
        Mark the current user as deleted for audit purposes.

        Raises:
            UserNotFoundError: If the user is not found.
            DatabaseServiceError: If a database operation fails.
        """
        rows = self.repository.find_by_filters(self.user.filters())
        verification_query = f"select * from users where {conditions}"
        try:
            rows = execute_query(verification_query, values)
            if not rows:
                raise UserNotFoundError("User not found, deletion aborted")
            if len(rows) > 1:
                raise ValueError("Deletion aborted due to multiple rows being found")
            delete_query = f"""
                            update user
                            set deleted = True
                            where {conditions}
                            """
            execute_query(delete_query, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to delete user") from e

    def can_borrow_book(self) -> bool:
        """
        Check if the current user is eligible to borrow a book.

        Returns:
            bool: True if the user has fewer than 5 books on loan, otherwise False.

        Raises:
            UserNotFoundError: If no user is found.
            DatabaseServiceError: If a database operation fails.
        """
        rows = self.repository.find_by_filters(self.user.filters())
        query = f"select * from users where {conditions}"
        try:
            get_user = execute_query(query, values)
            if not get_user:
                raise UserNotFoundError("User not found in the database")
            if get_user[0].get("books_loaned", 0) > 5:
                return False
            return True
        except Exception as e:
            raise DatabaseServiceError("Failed to retrieve borrow eligibility") from e

    def get_outstanding_late_fees(self) -> float:
        """
        Calculate the total outstanding late fees for the current user.

        Returns:
            float: The total late fees owed.

        Raises:
            ValueError: If the user is not found.
            DatabaseServiceError: If a database operation fails.
        """
        rows = self.repository.find_by_filters(self.user.filters())
        query = f"""
                select u.user_id, 
                u.first_name, 
                u.last_name,
                l.accumulated_late_fee 
                from users u
                left join loan l on u.user_id = l.user_id
                where {conditions}
                group by u.user_id, u.first_name, u.last_name
                """
        try:
            late_fee = execute_query(query, values)
            if not late_fee:
                raise ValueError("At least one filter must be passed in")
            total_fee = late_fee[0].get("l.accumulated_late_fee", 0)
            return total_fee
        except Exception as e:
            raise DatabaseServiceError(
                "Failed to retrieve outstanding late fees"
            ) from e

    def get_overdue_users(self) -> list[dict[str, Any]]:
        """
        Retrieve all users with overdue books.

        Returns:
            list[dict[str, Any]]: A list of users with overdue loans.

        Raises:
            DatabaseServiceError: If a database operation fails.
        """
        try:
            overdue = execute_query(
                """
                select u.first_name,
                       u.last_name,
                       u.email_address,
                       u.phone_number
                from users u
                left join loan l on l.user_id=u.user_id
                having l.overdue_return = True
                """
            )
            if overdue:
                return overdue
            else:
                return [{"no_overdue": "users_found"}]
        except Exception as e:
            raise DatabaseServiceError("Failed to retrieve overdue users") from e

    def get_books_on_loan(self) -> list[dict[str, Any]]:
        """
        Retrieve all books currently on loan for the user.

        Returns:
            list[dict[str, Any]]: A list of loaned books.

        Raises:
            UserNotFoundError: If no user is found.
            ValueError: If no books on loan are found.
            DatabaseServiceError: If a database operation fails.
        """
        rows = self.repository.find_by_filters(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        try:
            if not find_user_query:
                raise UserNotFoundError(
                    "Unable to find user, therefore unable to find books on loan"
                )
            find_books_query = f"select books_loaned from users where {conditions}"
            if not find_books_query:
                raise ValueError(
                    f"{self.user.first_name} {self.user.last_name} does not have any books on loan"
                )
            return execute_query(find_books_query, values) or []
        except Exception as e:
            raise DatabaseServiceError(
                f"Unable to see books on loan for {self.user.first_name} {self.user.last_name}"
            ) from e
