from __future__ import annotations
from data.classes.loan import Loan
from data.classes.book import Book
from data.classes.user import User
from data.database.dbconn import execute_query
from data.database.models import loan_insert, users_insert
from src.services.base_services import BaseService
from typing import Any


class LoanServices(BaseService):
    def __init__(self, loan: Loan, book: Book, user: User) -> None:
        self.loan = loan
        self.book = book
        self.user = user

    def borrow_book(self) -> None:
        """
        Class method for borrowing a book
        """
        self.loan.borrow_book()
        current_books_loaned: list[str] = []
        conditions, values = self.build_conditions(self.user.filters())
        books = execute_query(f"select books_loaned from users where {conditions}")
        if not books:
            current_books_loaned.append(self.book.title)
        else:
            for dictionaries in books:
                for _, v in dictionaries:
                    current_books_loaned.append(v)
            current_books_loaned.append(self.book.title)
            execute_query(
                users_insert,
            )
