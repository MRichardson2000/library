from data.database.sql_models import users_insert
from data.classes.user import User
from data.dataclasses.db_dataclass import DB
from data.database.dbconn import fetch_result, execute_query


class UserQueries:
    def __init__(self, db_session: DB) -> None:
        self.db_session = db_session

    def find_user(self, email_address: str) -> User | None:
        """
        Retrieves a user from the database by email address.

        Args:
            email_address: The email address to search for.

        Returns:
            A User object if found, None otherwise.
        """
        rows = fetch_result(
            "select * from user where email_address = :email_address",
            {"email_address": email_address},
            db_details=self.db_session,
        )
        return User.from_db_row(rows[0]) if rows else None

    def insert_user(self, user: User) -> None:
        """
        Inserts a new user into the database if not already present.

        Args:
            user: The User object to insert.
        """
        row = self.find_user(user.email_address)
        if not row:
            execute_query(users_insert, user.to_dict(), db_details=self.db_session)

    def set_surname(self, user: User) -> None:
        """
        Updates the surname of an existing user.

        Args:
            user: The User object with updated surname.
        """
        row = self.find_user(user.email_address)
        if row:
            execute_query(
                """
                update users
                set last_name = :last_name
                where first_name = :first_name
                and user_id = :user_id
                """,
                {"last_name": self},
                db_details=self.db_session,
            )

    def set_email(self, user: User) -> None:
        """
        Updates the email address of an existing user.

        Args:
            user: The User object with updated email address.
        """
        row = self.find_user(user.email_address)
        if row:
            execute_query(
                """
                update users
                set email_address = :email_address
                where first_name = :first_name
                and user_id = :user_id
                """,
                {
                    "email_address": user.email_address,
                    "first_name": user.first_name,
                    "user_id": user.user_id,
                },
                db_details=self.db_session,
            )

    def set_phone_number(self, user: User) -> None:
        """
        Updates the phone number of an existing user.

        Args:
            user: The User object with updated phone number.
        """
        row = self.find_user(user.email_address)
        if row:
            execute_query(
                """
                update users
                set phone_number = :phone_number
                where first_name = :first_name
                and user_id = :user_id
                """,
                {
                    "phone_number": user.phone_number,
                    "first_name": user.first_name,
                    "user_id": user.user_id,
                },
                db_details=self.db_session,
            )

    def set_status(self, user: User) -> None:
        """
        Updates the account status of an existing user.

        Args:
            user: The User object with updated account status.
        """
        row = self.find_user(user.email_address)
        if row:
            execute_query(
                """
                update users
                set account_state = :account_state
                where first_name = :first_name
                and user_id = :user_id
                """,
                {
                    "account_state": user.account_state,
                    "first_name": user.first_name,
                    "user_id": user.user_id,
                },
                db_details=self.db_session,
            )
