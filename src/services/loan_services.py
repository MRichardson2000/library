from __future__ import annotations
from data.database.sql_models import loan_insert
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
    UserNotFoundError,
    InvalidUserData,
    BookNotFoundError,
    InvalidBookData,
    InventoryNotFoundError,
    InventoryUpdateError,
)
import logging
from typing import Any


class LoanServices:
    def __init__(
        self,
        user: User,
        inventory: Inventory,
        book: Book,
        executor: LoanQueryExecutor,
        filters: FilterBuilder,
    ) -> None:
        self.user = user
        self.inventory = inventory
        self.book = book
        self.executor = executor
        self.filters = filters

    # def create_loan(self) -> None:
    #     '''
    #     Docstring for create_loan

    #     :param self: Description
    #     '''
    #     logging.info("Attempting to initiate a loan for book: %s for user: %s %s", self.book.title, self.user.first_name, self.user.last_name)
    #     book_conditions, book_values = self.filters.build_conditions(self.book.filters())
    #     book_query = f"select * from book where {book_conditions}"
    #     try:
    #         book_check = self.executor.execute(book_query, book_values)
    #         if not book_check:
    #             book_msg = "Book not found in the database. Please speak with the admins to register the book. Not eligible for loan until this is done!"
    #             logging.warning(book_msg)
    #             raise BookNotFoundError(book_msg)
    #         user_conditions, user_values = self.filters.build_conditions(self.user.filters())
    #         user_query = f"select * from users where {user_conditions}"
    #         user_check = self.executor.execute(user_query, user_values)
    #         if not user_check:
    #             usr_msg = "User not found in the database. Please make sure you register before attempting to borrow a book"
    #             logging.warning(usr_msg)
    #             raise UserNotFoundError(usr_msg)
    #         book_id = f"select book_id from book where {book_conditions}"
    #         user_id = f"select user_id from users where {user_conditions}"
