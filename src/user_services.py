from __future__ import annotations
from data.classes import User, Loan
from data.dbconn import execute_query
from data.models import users_insert
from typing import Any


class UserServices:
    def __init__(self) -> None:
        pass

    def create_user(self, user: User) -> bool:
        try:
            check_user = execute_query(
                """
                select * from users
                where first_name = :first_name,
                    and last_name = :last_name,
                    and email_address = :email_address,
                    and phone_number = :phone_number
                """,
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email_addres": user.email_address,
                    "phone_number": user.phone_number,
                },
            )
            user_insert_tuple = (
                user.first_name,
                user.last_name,
                user.email_address,
                user.phone_number,
                user.books_loaned,
            )
            if not check_user:
                execute_query(users_insert, user_insert_tuple)
                return True
        except Exception as e:
            raise e
        return False

    def get_user(self, user: User) -> list[dict[str, Any]] | None:
        try:
            filters: dict[str, Any] = user.filters()
            filters: dict[str, Any] = {
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
        try:
            filters: dict[str, Any] = user.filters()
            filters: dict[str, Any] = {
                k: v for k, v in filters.items() if v is not None
            }
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
        try:
            filters: dict[str, Any] = user.filters()
            filters: dict[str, Any] = {
                k: v for k, v in filters.items() if v is not None
            }
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
        

    def list_overdue_users(self) -> None:
        pass

    def audit_log(self) -> None:
        pass

    def find_top_borrowers(self) -> None:
        pass

    def longstanding_borrowers(self) -> None:
        pass
