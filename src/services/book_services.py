from __future__ import annotations
from data.classes.book import Book
from data.database.dbconn import execute_query
from data.database.models import book_insert
from typing import Any


class BookServices:
    def __init__(self) -> None:
        pass

    def create_book(self, book: Book) -> bool:
        """
        Creates a book object in the database using the book class if the book
        doesn't already exist.

        Args:
            book (Book): a book object. The class object is in data/classes/book.py

        Returns:
            bool: True if the book is created successfully or false

        Raises:
            Exception: Handles errors outside of our control. Database errors
            for example.

        Notes:
            This function will check if a book with the details passed in already
            exists. If it's found it returns false otherwise it creates the book
            object and adds it to the database.
        """
        try:
            filters: dict[str, Any] = book.filters()
            filters = {k: v for k, v in filters.items() if v is not None}
            conditions = " and ".join(
                [f"{k} = :{k}, {v} = %s" for k, v in filters.items()]
            )
            if not filters:
                raise ValueError("You need to enter all values when creating book.")
            book_check = execute_query(f"select * from book where {filters}")
            if not book_check:
                execute_query(book_insert, conditions)
                return True
        except Exception:
            raise
        return False
