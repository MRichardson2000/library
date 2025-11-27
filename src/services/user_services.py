from __future__ import annotations
from data.classes.user import User
from data.classes.loan import Loan
from data.database.dbconn import execute_query
from data.database.models import users_insert
from typing import Any


class UserServices:
    def __init__(self) -> None:
        pass

    def create_user(self, user: User) -> bool:
        """
        Create a new user record in the database if one does not exist already.

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:
            bool: True if the user was created and registered in the database successfully. Otherwise false

        Raises:
            Exception: handles any errors outside of our control - Database errors for example.

        Notes:
            This function will check if a user with the details passed in already exists, if a match isn't
            found it's added into the database. Otherwise it returns false and does nothing.
        """
        try:
            filters: dict[str, Any] = user.filters()
            filters = {k: v for k, v in filters.items() if v is not None}
            if not filters:
                raise ValueError("All filters are required for creating a user")
            user_check = execute_query(f"select * from users where {filters}")
            if not user_check:
                execute_query(users_insert, filters)
                return True
        except Exception as e:
            raise e
        return False

    def get_user(self, user: User) -> list[dict[str, Any]] | None:
        """
        Searches the database to get the details of the user passed in

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:
            list of dictionarys containing a string and then Any.

        Raises:
            Exception: handles any errors outside of our control - Database errors for example.

        Notes:
            This function uses a dictionary comprehension to create a new dictionary which removes
            None values. We then pull from the database using the details passed in. It will return
            a user and their assosciated information.
        """
        try:
            filters: dict[str, Any] = user.filters()
            filters = {
                **{k: v for k, v in filters.items() if v is not None},
                "books_loaned": user.books_loaned,
            }
            conditions = " and ".join([f"{k} = :{k}" for k in filters.keys()])
            user_details = f"""
                select * from users where {conditions}
                """
            return execute_query(user_details, filters)
        except Exception as e:
            raise e

    def delete_user(self, user: User) -> bool:
        """
        Attempts to delete a user from the database

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:
            bool: True if the user was successfully deleted otherwise false. Raises
            an error if no matching user is found or if multiple matches exist.

        Raises:
            ValueError: If no filters are provided, if the query returns no results, or if multiple rows are found.
            Exception: For unexpected errors outside of our control such as database related issues

        Notes:
        A dictionary comprehension is used to remove None values from the filters before building the query.
        The function first verifies the existence of the user before attempting deletion.
        Deletion only proceeds if exactly one matching user is found.
        """
        try:
            filters: dict[str, Any] = user.filters()
            filters = {k: v for k, v in filters.items() if v is not None}
            if not filters:
                raise ValueError("At least one filter must be provided")
            conditions = " and ".join([f"{k} = %s" for k in filters.keys()])
            values = list(filters.values())
            deletion_verification = f"select * from users where {conditions}"
            rows = execute_query(deletion_verification, values)
            if not rows:
                raise ValueError("Query returned no results")
            if len(rows) == 1:
                delete_query = f"delete from users where {conditions}"
                execute_query(delete_query, values)
                return True
            else:
                raise ValueError("Deletion aborted due to multiple rows being found")
        except Exception:
            raise

    def check_borrow_eligibility(self, user: User) -> bool:
        """
        .

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:


        Raises:


        Notes:

        """
        try:
            filters: dict[str, Any] = user.filters()
            filters = {k: v for k, v in filters.items() if v is not None}
            if not filters:
                raise ValueError("At least one filter must be provided")
            conditions = " and ".join([f"{k} = %s" for k in filters.keys()])
            get_books = execute_query(f"select * from users where {conditions}")
            if get_books:
                for row in get_books:
                    if len(row) > 5:
                        return False
            return True
        except Exception:
            raise

    def calculate_outstanding_late_fees(self, user: User, loan: Loan) -> float:
        """
        .

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:


        Raises:


        Notes:

        """
        try:
            filters: dict[str, Any] = user.filters()
            filters = {k: v for k, v in filters.items() if v is not None}
            if not filters:
                raise ValueError("At least one filter must be provided")
            conditions = " and ".join([f"{k} = %s" for k in filters.keys()])

        except Exception:
            raise

    def list_overdue_users(self) -> None:
        """
        .

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:


        Raises:


        Notes:

        """
        pass

    def audit_log(self) -> None:
        """
        .

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:


        Raises:


        Notes:

        """
        pass

    def find_top_borrowers(self) -> None:
        """
        .

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:


        Raises:


        Notes:

        """
        pass

    def longstanding_borrowers(self) -> None:
        """
        .

        Args:
            user (User): a User object - the class object is in data - classes - user.py

        Returns:


        Raises:


        Notes:

        """
        pass
