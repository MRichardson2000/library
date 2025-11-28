from __future__ import annotations
from data.classes.user import User

# from data.classes.loan import Loan
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
            conditions = " and ".join(
                [f"{k} = :{k}, {v} = %s" for k, v in filters.items()]
            )
            if not filters:
                raise ValueError("All filters are required for creating a user")
            user_check = execute_query(f"select * from users where {filters}")
            if not user_check:
                execute_query(users_insert, conditions)
                return True
        except Exception as e:
            raise e
        return False

    def get_user_details(self, user: User) -> list[dict[str, Any]] | None:
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
            filters = {k: v for k, v in filters.items() if v is not None}
            if not filters:
                raise ValueError(
                    "You need to pass in at least one value to get the details of a user"
                )
            conditions = " and ".join([f"{k} = %s" for k in filters.keys()])
            user_details = f"select * from users where {conditions}"
            values = tuple(filters.values())
            return execute_query(user_details, values)
        except Exception:
            raise

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
                raise ValueError("Delete user query returned no results")
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
