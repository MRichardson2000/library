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
    def __init__(self) -> None:
        pass

    def create_user(self, user: User) -> None:
        """
        Create a new user record in the database if one does not exist already.

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:
            None: It just creates the user

        Raises:
            UserAlreadyExistsError: If the user already exists
            DatabaseServiceError: for andy database errors
            Exception: Anything else

        Notes:
            This function will check if a user with the details passed in already exists, if a match isn't found it's added into the database.
        """
        conditions, values = self.build_conditions(user.filters())
        query = f"select * from users where {conditions}"
        user_check = execute_query(query, values)
        if user_check:
            raise UserAlreadyExistsError("User already exists")
        try:
            execute_query(users_insert, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to create user") from e

    def get_user_details(self, user: User) -> list[dict[str, Any]]:
        """
        Searches the database to get the details of the user passed in

        Args:
            user (User): a User object - the class object is in data - classes - user.py

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
        conditions, values = self.build_conditions(user.filters())
        query = f"select * from users where {conditions}"
        try:
            get_user = execute_query(query, values)
            if not get_user:
                raise UserNotFoundError("User not found in the database")
            return get_user
        except Exception as e:
            raise DatabaseServiceError("Failed to retrieve user details") from e

    def delete_user(self, user: User) -> None:
        """
        This functions updates the deleted column in the database to True. The user is
        still in the system for audit purposes they are just marked as deleted.

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:
            None: It just updates the deleted column in the database

        Raises:

        Notes:

        """

        conditions, values = self.build_conditions(user.filters())
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

    def check_borrow_eligibility(self, user: User) -> bool:
        """
        Checks if someone is eligible to borrow a book. The current loan limit is 5 books

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:
            bool: Either true or false if they already have 5 loaned books

        Raises:
            ValueError: if no filters are provided
            Exception: if an error outside of our control happens

        Notes:
            We find the users and then look for the books loaned column. If the value is
            greater than 5 then they're at max capacity and need to return a book before
            they can loan another. The max is 5.

        """
        try:
            filters: dict[str, Any] = user.filters()
            filters = {k: v for k, v in filters.items() if v is not None}
            if not filters:
                raise ValueError("At least one filter must be provided")
            conditions = " and ".join([f"{k} = %s" for k in filters.keys()])
            values = list(filters.values())
            get_user = execute_query(f"select * from users where {conditions}", values)
            if get_user and get_user[0].get("books_loaned", 0) > 5:
                return False
            return True
        except Exception:
            raise

    def calculate_outstanding_late_fees(self, user: User) -> float:
        """
        Calculate the total outstanding late fees for a given user.

        This method builds a SQL query based on the filters provided by the
        `User` object, retrieves the accumulated late fees from the `loan`
        table, and returns the total amount owed. If no filters are provided,
        a ValueError is raised. If no matching records are found, the method
        returns 0.0.

        Args:
            user (User): A User object (defined in `data/classes/user.py`)
                that provides filter criteria through its `filters()` method.

        Returns:
            float: The total outstanding late fee for the user. Returns 0.0
            if no records are found.

        Raises:
            ValueError: If no filters are provided by the User object.
            Exception: Propagates any exceptions raised during query execution.

        Notes:
            - The query joins the `users` table with the `loan` table on
            `user_id`.
            - Filters are dynamically applied to the WHERE clause based on
            non-null values returned by `user.filters()`.
            - The query groups results by user details to ensure unique
            aggregation.
        """

        try:
            filters: dict[str, Any] = user.filters()
            filters = {k: v for k, v in filters.items() if v is not None}
            if not filters:
                raise ValueError("At least one filter must be provided")
            conditions = " and ".join([f"{k} = %s" for k in filters.keys()])
            values = list(filters.values())
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
            result = execute_query(query, values)
            if result:
                total_fee = result[0].get("l.accumulated_late_fee", 0)
                return total_fee
        except Exception:
            raise
        return 0.0

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
            Exception: To handle if there's an error with the database connection
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
        except Exception:
            raise
