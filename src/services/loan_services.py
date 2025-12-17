from __future__ import annotations
from datetime import datetime
from data.database.queries.loan_queries import LoanQueries
from data.classes.loan import Loan
from data.classes.book import Book
from data.classes.user import User
from data.classes.inventory import Inventory
from data.classes.loan import Loan
from src.services.exceptions import (
    DatabaseServiceError,
)
from typing import Any


class LoanServices:
    def __init__(
        self,
        user: User,
        loan: Loan,
        loan_queries: LoanQueries,
        inventory: Inventory,
        book: Book,
    ) -> None:
        self.user = user
        self.loan = loan
        self.loan_queries = loan_queries
        self.inventory = inventory
        self.book = book

    def start_loan_transaction(self) -> None:
        self.loan.borrow_book()
        try:
            self.loan_queries.insert_loan()
        except Exception as e:
            raise DatabaseServiceError("Failed to start loan transaction") from e

    def end_loan_transaction(self) -> None:
        self.loan.return_book()
        try:
            self.loan_queries.end_loan()
        except Exception as e:
            raise DatabaseServiceError("Failed to end loan transaction") from e

    def loaned_books(self) -> list[dict[str, Any]] | None:
        try:
            self.loan_queries.get_books_on_loan()
        except Exception as e:
            raise DatabaseServiceError(
                "Failed to retrieve books on loan for user"
            ) from e

    def extend_loan_transaction(self) -> None:
        self.loan.extend_loan()
        try:
            self.loan_queries.loan_extension()
        except Exception as e:
            raise DatabaseServiceError("Failed to extend loan") from e

    def verify_loan_permissions(self) -> bool:
        """all verification stats can be created and then added to the verification module"""
        try:
            self.loan_queries.verification()
        except Exception as e:
            raise DatabaseServiceError("Failed to verify loan permissions") from e
        return False

    def retrieve_due_date(self) -> datetime | None:
        try:
            self.loan_queries.due_date_retrieval()
        except Exception as e:
            raise DatabaseServiceError("Failed to retrieve due_date") from e
