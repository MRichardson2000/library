from __future__ import annotations
from data.classes.user import User
from data.database.dbconn import execute_query
from data.database.models import users_insert
from src.services.base_services import BaseService
from src.services.exceptions import (
    UserAlreadyExistsError,
    DatabaseServiceError,
    UserNotFoundError,
)
from typing import Any


class UserServices(BaseService):
    def __init__(self, user: User) -> None:
        self.user = user

    def create_user(self) -> None:
        """
        Create a new user record in the database if one does not exist already.

        Args:
            user (User): Initialised in the init method:  a User object - the class object is in data - classes - user.py

        Returns:
            None: It just creates the user

        Raises:
            UserAlreadyExistsError: If the user already exists
            DatabaseServiceError: for andy database errors
            Exception: Anything else

        Notes:
            This function will check if a user with the details passed in already exists, if a match isn't found it's added into the database.
        """
        conditions, values = self.build_conditions(self.user.filters())
        query = f"select * from users where {conditions}"
        user_check = execute_query(query, values)
        if user_check:
            raise UserAlreadyExistsError("User already exists")
        try:
            execute_query(users_insert, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to create user") from e

    def get_user_details(self) -> list[dict[str, Any]]:
        """
        Searches the database to get the details of the user passed in

        Args:
            user (User): Initialised in the init method:  a User object - the class object is in data - classes - user.py

        Returns:
            list[dict[str, Any]]: - a sql row with the user information

        Raises:
            UserNotFoundError: If the user is not found in the database
            DatabaseServiceErrror: If there's an issue outside of our control e.g. a database
            error
            Exception: Anything else

        Notes:
            This function checks if a user exists with the details passed in. If a user
            is found, the details of that user are returned.
        """
        conditions, values = self.build_conditions(self.user.filters())
        query = f"select * from users where {conditions}"
        try:
            get_user = execute_query(query, values)
            if not get_user:
                raise UserNotFoundError("User not found in the database")
            return get_user
        except Exception as e:
            raise DatabaseServiceError("Failed to retrieve user details") from e

    def change_surname(self, new_surname: str) -> None:
        conditions, values = self.build_conditions(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        last_name = self.user.last_name
        last_name = new_surname
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
                            set last_name = {last_name}
                            where {conditions}
                            """
            execute_query(update_query)
        except Exception as e:
            raise DatabaseServiceError("Failed to change users surname") from e

    def new_email(self, new_email_address: str) -> None:
        conditions, values = self.build_conditions(self.user.filters())
        find_user_query = f"select * from users where {conditions}"
        email = self.user.email_address
        email = new_email_address
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
                            set email_address = {email}
                            where {conditions}
                            """
            execute_query(update_query)
        except Exception as e:
            raise DatabaseServiceError("Failed to change email address") from e

    def delete_user(self) -> None:
        """
        This functions updates the deleted column in the database to True. The user is
        still in the system for audit purposes they are just marked as deleted.

        Args:
            user (User): Initialised in the init method:  a User object - the class object is in data - classes - user.py

        Returns:
            None: It just updates the deleted column in the database

        Raises:
            UserNotFoundError: If the user doesn't exist in the database
            DatabaseServiceError: Database errors outside of our control
            Exception: Anything else

        Notes:
            We check if the users there, if they are we check and make sure only 1 row is pulled from the database, if multiple rows are pulled the deletion
            aborts as only 1 should be visible. then we update the deleted field to true for that user.

        """

        conditions, values = self.build_conditions(self.user.filters())
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

    def check_borrow_eligibility(self) -> bool:
        """
        Checks if someone is eligible to borrow a book. The current loan limit is 5 books but this can be modified

        Args:
            user (User): Initialised in the init method:  a User object - the class object is in data - classes - user.py

        Returns:
            bool: Either true or false if they already have 5 loaned books

        Raises:
            UserNotFoundError: if no user is found in the database
            DatabaseServiceError: If there's an issue outside of our control involving the database
            Exception: Anything else

        Notes:
            We find the users and then look for the books loaned column. If the value is
            greater than 5 then they're at max capacity and need to return a book before
            they can loan another. The max is 5.

        """
        conditions, values = self.build_conditions(self.user.filters())
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

    def calculate_outstanding_late_fees(self) -> float:
        """
        Calculate the total outstanding late fees for a given user.

        This method builds a SQL query based on the filters provided by the
        User object, retrieves the accumulated late fees from the loan
        tables accumulated fees column, and returns the total amount owed.

        Args:
            user (User): Initialised in the init method:  A User object defined in data/classes/user.py
                that provides filter criteria through its filters() method.

        Returns:
            float: The total outstanding late fee for the user.

        Raises:
            DatabaseServiceError: if there's an issue outside of our control with the database connection.
            ValueError: If the user is not found
            Exception: Propagates any exceptions raised during query execution.

        Notes:
            The query joins the users table with the loan table on
            user_id.
            Filters are dynamically applied to the WHERE clause based on
            non-null values returned by self.user.filters().
            The query then shows the outstanding late fees
        """
        conditions, values = self.build_conditions(self.user.filters())
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

    def list_overdue_users(self) -> list[dict[str, Any]]:
        """
        Retrieves all users from the database that have overdue books that
        need returning.

        Args:
            No args here, just a query to pull data out that lists users who
            late books that need handing in.

        Returns:
            list[dict[str, Any]]: returns with details if any are present.
            Otherwise it returns an empty list of dicts that states no
            values were found.

        Raises:
            Exception: Anything else
            DatabaseServiceError: To handle if there's an error with the database connection
            that's outside of our control

        Notes:
            Simple yet effective query to list the users that have overdue_returns
            resulting in late fees due to be paid.

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
