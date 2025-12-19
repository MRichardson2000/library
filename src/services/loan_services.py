from __future__ import annotations
from datetime import datetime
from data.database.queries.loan_queries import LoanQueries
from data.classes.loan import Loan
from data.classes.book import Book
from data.classes.user import User
from data.classes.inventory import Inventory
from src.services.exceptions import (
    DatabaseServiceError,
)
from typing import Any
import logging


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
        """
        Initiates a new loan transaction for the user to borrow a book.
        """
        logging.info(
            "Attempting to start loan transaction of %s for %s %s",
            self.book.title,
            self.user.first_name,
            self.user.last_name,
        )
        self.loan.borrow_book()
        try:
            self.loan_queries.insert_loan(self.book)
            logging.info(
                "Successfully initiated loan transactionfor %s %s",
                self.user.first_name,
                self.user.last_name,
            )
        except Exception as e:
            logging.exception("Failed to start loan transaction")
            raise DatabaseServiceError("Failed to start loan transaction") from e

    def end_loan_transaction(self) -> None:
        """
        Terminates an existing loan transaction for the user returning a book.
        """
        logging.info(
            "Attempting to end loan transaction of %s for %s %s",
            self.book.title,
            self.user.first_name,
            self.user.last_name,
        )
        self.loan.return_book()
        try:
            self.loan_queries.end_loan(self.book)
            logging.info("Successfully ended loan transaction")
        except Exception as e:
            logging.exception("Failed to end loan transaction")
            raise DatabaseServiceError("Failed to end loan transaction") from e

    def get_loaned_books(self) -> list[dict[str, Any]] | None:
        """
        Retrieves a list of all books currently on loan for the user.
        """
        logging.info(
            "Attempting to retrieve the books on loan for %s %s",
            self.user.first_name,
            self.user.last_name,
        )
        try:
            self.loan_queries.get_books_on_loan(self.user)
            logging.info(
                "Successfully retrieved books on loan for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
        except Exception as e:
            logging.exception(
                "Failed to retrieve books on loan for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
            raise DatabaseServiceError(
                "Failed to retrieve books on loan for %s %s",
                self.user.first_name,
                self.user.last_name,
            ) from e

    def extend_loan_transaction(self) -> None:
        """
        Extends the loan period for a currently borrowed book.
        """
        logging.info("Attempting to extend loan transaction for %s", self.book.title)
        self.loan.extend_loan()
        try:
            logging.info(
                "Successfully extended loan transaction for %s", self.book.title
            )
            self.loan_queries.loan_extension(self.loan)
        except Exception as e:
            logging.exception("Failed to extend loan of %s", self.book.title)
            raise DatabaseServiceError(
                "Failed to extend loan of %s", self.book.title
            ) from e

    def verify_loan_permissions(self) -> bool:
        """
        Verifies that the user has permission to borrow the book.
        """
        logging.info(
            "Check in progress to verify %s %s has permission to loan %s",
            self.user.first_name,
            self.user.last_name,
            self.book.title,
        )
        try:
            self.loan_queries.verification(self.user)
            logging.info("Verification checks completed successfully")
        except Exception as e:
            logging.exception(
                "Failed to verify loan permissions for %s %s",
                self.user.first_name,
                self.user.last_name,
            )
            raise DatabaseServiceError("Failed to verify loan permissions") from e
        return False

    def get_due_date(self) -> datetime | None:
        """
        Retrieves the due date for a currently borrowed book.
        """
        logging.info("Attempting to get due date of %s", self.book.title)
        try:
            self.loan_queries.due_date_retrieval(self.book)
            logging.info("Successfully retrieved due date for %s", self.book.title)
        except Exception as e:
            logging.exception("Failed to retrive due date of %s", self.book.title)
            raise DatabaseServiceError("Failed to retrieve due_date") from e
