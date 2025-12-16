from __future__ import annotations
from datetime import datetime
from data.database.dbconn import execute_query, fetch_result
from data.database.query import FIND_BY_TITLE
from data.database.sql_models import loan_insert
from data.classes.loan import Loan
from data.classes.book import Book
from data.classes.user import User
from data.classes.inventory import Inventory
from data.classes.loan import Loan
from src.services.exceptions import (
    BookNotFoundError,
    DatabaseServiceError,
)
from typing import Any


class LoanServices:
    def __init__(
        self,
        user: User,
        loan: Loan,
        inventory: Inventory,
        book: Book,
    ) -> None:
        self.user = user
        self.loan = loan
        self.inventory = inventory
        self.book = book

    def start_loan_transaction(self) -> None:
        """
        Initiate a loan transaction for a book.

        This method attempts to create a new loan record for a user to borrow a book.
        It performs the following steps:
        1. Validates that the book exists in the database
        2. Creates a loan record in the database
        3. Removes the book from inventory stock

        Raises:
            BookNotFoundError: If the book is not found in the database.
            DatabaseServiceError: If any database operation fails during the loan initiation process.

        Note:
            - Logs information about the loan initiation attempt
            - Logs a warning if the book is not found
            - Logs an exception if the database operation fails
        """
        self.loan.borrow_book()
        try:
            book_row = fetch_result(FIND_BY_TITLE, {"title": self.book.title})
            if not book_row:
                raise BookNotFoundError()
            if len(book_row) > 1:
                raise ValueError("Multiple rows found, unable to initiate loan")
            execute_query(loan_insert, self.book.to_dict())
        except Exception as e:
            raise DatabaseServiceError("Failed to start loan transaction") from e

    def end_loan_transaction(self) -> None:
        """
        Docstring for end_loan_transaction

        :param self: Description
        """
        self.loan.return_book()
        try:
            loan_row = fetch_result(FIND_BY_TITLE, {"title": self.book.title})
            if not loan_row:
                raise BookNotFoundError()
            if len(loan_row) > 1:
                raise ValueError(
                    "Unable to end loan transaction, multiple rows detected"
                )
            execute_query("update loan set ")  # finish later
        except Exception as e:
            raise DatabaseServiceError("Failed to end loan transaction") from e

    def loaned_books(self) -> list[dict[str, Any]] | None:
        query = ""  # finish later
        try:
            fetch_result(query)
        except Exception as e:
            raise DatabaseServiceError(
                "Failed to retrieve books on loan for user"
            ) from e

    def extend_loan(self) -> None:
        self.extend_loan()
        try:
            execute_query(
                "update loan set due_date = :due_date", {"due_date": self.loan.due_date}
            )
        except Exception as e:
            raise DatabaseServiceError("Failed to extend loan") from e

    def verify_loan_permissions(self) -> bool:
        """
        requirements 5 books max, no late fees due, no late return books
        """
        max_books = ""  # fill in later
        books_returned_late = ""  # fill in later
        late_fees = ""  # fill in later
        try:
            books = fetch_result(max_books)
            if not books[0]:
                late_returns = fetch_result(books_returned_late)
                if not late_returns:
                    late_fees = fetch_result(late_fees)
                    if not late_fees:
                        return True
        except Exception as e:
            raise DatabaseServiceError("Failed to verify loan permissions") from e
        return False

    def retrieve_due_date(self) -> datetime | None:
        try:
            due_date = fetch_result(
                "select * from loan where book_id = :book_id and status = 'Borrowed'",
                {"title": self.book.title},
            )
            if len(due_date) == 1:
                return due_date[0]["due_date"]
        except Exception as e:
            raise DatabaseServiceError("Failed to retrieve due_date") from e
