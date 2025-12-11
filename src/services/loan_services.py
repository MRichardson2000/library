from __future__ import annotations
from datetime import datetime, timedelta
from data.database.sql_models import loan_insert
from data.classes.loan import Loan
from data.classes.book import Book
from data.classes.user import User
from data.classes.inventory import Inventory
from data.classes.loan import Loan
from src.services.base_services import LoanQueryExecutor, FilterBuilder
from src.services.exceptions import (
    LoanAlreadyExistsError,
    LoanLimitExceededError,
    LoanNotFoundError,
    LoanOverdueError,
    BookNotFoundError,
    InvalidBookData,
    InventoryNotFoundError,
    InventoryUpdateError,
    DatabaseServiceError,
)
import logging
from typing import Any


class LoanServices:
    def __init__(
        self,
        user: User,
        loan: Loan,
        inventory: Inventory,
        book: Book,
        executor: LoanQueryExecutor,
        filters: FilterBuilder,
    ) -> None:
        self.user = user
        self.loan = loan
        self.inventory = inventory
        self.book = book
        self.executor = executor
        self.filters = filters

    def start_loan_transaction(self) -> None:
        """
        Initiate a loan and store the details in the database

        Raises:
            BookNotFoundError: If a book is not found in the database.
            DatabaseServiceError: If a database operation fails.
        """
        logging.info(
            "Attempting to initiate a loan for book: %s for user: %s %s",
            self.book.title,
            self.user.first_name,
            self.user.last_name,
        )
        book_conditions, book_values = self.filters.build_conditions(
            self.book.filters()
        )
        book_query = f"select * from book where {book_conditions}"
        try:
            book_check = self.executor.execute(book_query, book_values)
            if not book_check:
                book_msg = "Book not found in the database. Please speak with the admins to register the book. Not eligible for loan until this is done!"
                logging.warning(book_msg)
                raise BookNotFoundError(book_msg)
            loan_values = self.loan.filters()
            self.executor.execute(loan_insert, loan_values)
            self.inventory.remove_stock()
            logging.info("Loan Successfully initiated.")
        except Exception as e:
            err_msg = "Failed to initiate loan for book: %s", self.book.title
            logging.exception(err_msg)
            raise DatabaseServiceError(err_msg) from e

    def end_loan_transaction(self) -> None:
        """
        Docstring for end_loan_transaction

        :param self: Description
        """
        logging.info(
            "Attempting to end a loan transaction for book: %s for user %s %s",
            self.book.title,
            self.user.first_name,
            self.user.last_name,
        )
        book_conditions, book_values = self.filters.build_conditions(
            self.book.filters()
        )
        book_query = f"select * from book where {book_conditions}"
        try:
            book_check = self.executor.execute(book_query, book_values)
            if not book_check:
                not_found_msg = "Book not found in the database. Please speak with the admins to register the book. Not eligible for loan until this is done!"
                logging.warning(not_found_msg)
                raise BookNotFoundError(not_found_msg)
            book_id = book_check[0]["book_id"]
            loan_check_query = (
                f"""
                                select *
                                from loan
                                where book_id = :book_id
                                and status = 'Borrowed'
                                and return_date is null
                                """,
                book_id,
            )
            if not loan_check_query:
                loan_msg = "%s is currently not loaned by anyone", self.book.title
                logging.warning(loan_msg)
                raise LoanNotFoundError(loan_msg)
            update_query = """
                            update loan
                            set status = 'Returned',
                                return_date = :return_date
                            where book_id = :book_id
                            and status = 'Borrowed'
                            and return date is null
                            """
            update_values: dict[str, Any] = {
                "book_id": self.book.book_id,
                "return_date": self.loan.return_date or datetime.now(),
            }
            self.executor.execute(update_query, update_values)
            self.inventory.remove_stock()
            logging.info(
                "The loan has been ended. %s: is now marked as returned in the database",
                self.book.title,
            )
        except Exception as e:
            err_msg = "Failed to end loan transaction"
            logging.exception(err_msg)
            raise DatabaseServiceError(err_msg) from e

    def loaned_books(self) -> list[dict[str, Any]] | None:
        """
        Attempts to retrieve books on loan for a user

        Raises database service error for database interaction errors
        """
        logging.info(
            "Attempting to retrieve the books on loan for user: %s",
            self.user.first_name,
        )
        query = """
                select u.first_name,
                       u.last_name,
                       b.title,
                       l.loan_time,
                       l.due_date
                from loan l
                left join users u on l.user_id = u.user_id
                left join book b on b.book_id = u.user_id
                where l.user_id = :user_id
                    and l.status = 'Borrowed'
                    and l.return_date is null
                """
        try:
            book_list = self.executor.execute(query)
            if book_list:
                logging.info(
                    "Successfully retrieved books on loan for %s", self.user.first_name
                )
                return book_list
        except Exception as e:
            err_msg = "Failed to retrieve books on loan for %s", self.user.first_name
            logging.exception(err_msg)
            raise DatabaseServiceError(err_msg) from e

    def extend_loan(self) -> None:
        """
        Attemps to extend the book on loan by 30 days. The days can be adjusted if needed

        Raises:
            BookNotFoundError if no book is found
            LoanNotFoundError if no loan is found
            DatabaseServiceError for any database related errors
        """
        logging.info(
            "Attempting to extend loan time for book: %s for user: %s %s",
            self.book.title,
            self.user.first_name,
            self.user.last_name,
        )
        book_conditions, book_values = self.filters.build_conditions(
            self.book.filters()
        )
        book_query = f"select * from book where {book_conditions}"
        try:
            book_check = self.executor.execute(book_query, book_values)
            if not book_check:
                not_found_msg = "Book not found in the database. Please speak with the admins to register the book. Not eligible for extension until this is done!"
                logging.warning(not_found_msg)
                raise BookNotFoundError(not_found_msg)
            book_id = book_check[0]["book_id"]
            loan_check_query = (
                f"""
                select *
                from loan
                where book_id = :book_id
                and status = 'Borrowed'
                and return_date is null
                """,
                book_id,
            )
            if not loan_check_query:
                loan_msg = (
                    "%s is currently not loaned by anyone, unable to extend the loan",
                    self.book.title,
                )
                logging.warning(loan_msg)
                raise LoanNotFoundError(loan_msg)
            self.loan.extend_loan(30)
            update_query = """
                            update loan
                            set due_date = :due_date
                            where book_id = :book_id
                            and status = 'Borrowed'
                            """
            update_values: dict[str, Any] = {
                "book_id": self.book.book_id,
                "due_date": self.loan.due_date,
            }
            self.executor.execute(update_query, update_values)
            logging.info("The loan has been extended by 30 days")
        except Exception as e:
            err_msg = (
                "Unable to extend loan for book: %s for user: %s %s",
                self.book.title,
                self.user.first_name,
                self.user.last_name,
            )
            logging.exception(err_msg)
            raise DatabaseServiceError(err_msg) from e

    def verify_loan_permissions(self) -> bool:
        """
        Check if the user has any constraints which restricts them from loaning another book.

        Raises:
        """
        logging.info(
            "Checking to see if %s %s is permitted to loan %s",
            self.user.first_name,
            self.user.last_name,
            self.book.title,
        )
        get_loaned_books = """
                            select u.user_id, b.book_id, b.title
                            from loan l
                            left join book b on l.book_id = b.book_id
                            left join users u on l.user_id = u.user_id
                            where l.status = 'Borrowed'
                                and u.user_id = :user_id
                            """
        try:
            rows = self.executor.execute(get_loaned_books)
            if len(rows) == 5:
                pass
        except Exception as e:
            pass
