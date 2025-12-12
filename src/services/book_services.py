from __future__ import annotations
from data.classes.book import Book
from data.classes.enums import BookState
from data.database.sql_models import book_insert
from data.database.query import FIND_BY_TITLE
from data.database.dbconn import execute_query, fetch_result
from data.classes.book import Book
from src.services.exceptions import (
    DatabaseServiceError,
    BookNotFoundError,
)
import logging
from typing import Any


class BookServices:
    def __init__(self, book: Book) -> None:
        self.book = book

    def create_book(self) -> None:
        """
        Create a new book record in the database if it does not already exist.

        Raises:
            BookAlreadyExistsError: If a book with the same details exists.
            DatabaseServiceError: If a database operation fails.
        """
        logging.info("Attempting to create book: %s", self.book.title)
        try:
            row = fetch_result(FIND_BY_TITLE, {"title": self.book.title})
            if not row:
                execute_query(book_insert, self.book.to_dict())
                logging.info("Book added to the database successfully")
        except Exception as e:
            logging.exception("Failed to create book")
            raise DatabaseServiceError("Failed to create book") from e

    def get_book_details(self) -> dict[str, Any]:
        """
        Retrieve details of the current book from the database.

        Returns:
            list[dict[str, Any]]: A list of matching book records.

        Raises:
            BookNotFoundError: If no book is found.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_TITLE, {"title": self.book.title})
            return row[0]
        except Exception as e:
            raise DatabaseServiceError("Failed to get book details") from e

    def delete_book(self) -> None:
        """
        Mark the current book as deleted and update inventory availability.

        Raises:
            ValueError: If no filters are provided, no results are found, or multiple matches exist.
            BookNotFoundError: If the book is not found in the database.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_TITLE, {"title": self.book.title})
            if not row:
                raise BookNotFoundError()
            if len(row) > 1:
                raise ValueError("Multiple rows returned, deletion aborted")
            self.book.status = BookState.DELETED
            execute_query(
                "update book set status = :status", {"status": self.book.status}
            )
        except Exception as e:
            raise DatabaseServiceError("Failed to mark book as deleted") from e

    def restore_book(self) -> None:
        """
        Mark the deleted column as false for the book in the database

        Raises:
            ValueError: If no results are found or multiple matches exist.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_TITLE, {"title": self.book.title})
            if not row:
                raise BookNotFoundError()
            if len(row) > 1:
                raise ValueError("Multiple rows returned, restore aborted")
            self.book.status = BookState.AVAILABLE
            execute_query(
                "update book set status = :status", {"status": self.book.status}
            )
        except Exception as e:
            raise DatabaseServiceError("Failed to mark book as restored") from e

    def update_book_rating(self, new_rating: int) -> None:
        """
        Update the rating of the current book in the database.

        Args:
            new_rating (int): The new rating value.

        Raises:
            ValueError: If no results are found or multiple matches exist.
            DatabaseServiceError: If a database operation fails.
        """
        try:
            row = fetch_result(FIND_BY_TITLE, {"title": self.book.title})
            if not row:
                raise BookNotFoundError()
            if len(row) > 1:
                raise ValueError(
                    "Modification aborted due to multiple rows being found"
                )
            self.book.rating = new_rating
            execute_query(
                "update book set rating = :rating", {"rating": self.book.rating}
            )
        except Exception as e:
            raise DatabaseServiceError("Failed to update book rating") from e
