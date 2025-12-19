from data.database.sql_models import loan_insert
from data.classes.book import Book
from data.classes.user import User
from data.classes.loan import Loan
from data.dataclasses.db_dataclass import DB
from data.database.dbconn import fetch_result, execute_query
from datetime import datetime
from typing import Any


class LoanQueries:
    def __init__(self, db_session: DB) -> None:
        self.db_session = db_session

    def insert_loan(self, book: Book) -> None:
        """
        Insert a new loan record for a book.
        """
        execute_query(loan_insert, book.to_dict(), db_details=self.db_session)

    def end_loan(self, book: Book) -> None:
        """
        Mark a loan as returned for a given book.
        """
        execute_query(
            """
            update loan
            set status = returned
            where book_id = :book_id
            """,
            {"book_id": book.book_id},
            db_details=self.db_session,
        )

    def get_books_on_loan(self, user: User) -> list[dict[str, Any]] | None:
        """
        Retrieve all books currently on loan for a user.
        """
        rows = execute_query(
            """
            select b.title
                   from loan l
                   left join book b on l.book_id = b.book_id
                   left join users u on l.user_id = u.user_id
                   where l.status = 'Borrowed'
                   and u.first_name = :first_name
                   and u.last_name = :last_name
            """,
            {"first_name": user.first_name, "last_name": user.last_name},
            db_details=self.db_session,
        )
        if rows:
            return rows

    def loan_extension(self, loan: Loan) -> None:
        """
        Extend the due date of an existing loan.
        """
        execute_query(
            "update loan set due_date = :due_date",
            {"due_date": loan.due_date},
            db_details=self.db_session,
        )

    def due_date_retrieval(self, book: Book) -> datetime | None:
        """
        Retrieve the due date for a borrowed book.
        """
        rows = fetch_result(
            "select due_date from loan where book_id = :book_id and status = 'Borrowed'",
            {"title": book.title},
            db_details=self.db_session,
        )
        if rows:
            values = rows[0].get("due_date")
            return values

    def verification(self, user: User) -> None:
        """
        Verify loan eligibility for a user.
        """
        self.max_book_number_check(user)

    def max_book_number_check(self, user: User) -> bool:
        """
        Check if user has exceeded the maximum loan limit of 5 books.
        """
        rows = fetch_result(
            """
            select b.title
                from loan l
                left join book b on l.book_id = b.book_id
                left join users u on l.user_id = u.user_id
                where l.status = 'Borrowed'
                and u.first_name = :first_name
                and u.last_name = :last_name
            """,
            {"first_name": user.first_name, "last_name": user.last_name},
            db_details=self.db_session,
        )
        books = [book for book in rows]
        return False if len(books) <= 5 else True
