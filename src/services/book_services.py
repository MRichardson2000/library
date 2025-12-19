from __future__ import annotations
from data.classes.book import Book
from data.classes.enums import BookState
from data.database.queries.book_queries import BookQueries
from data.classes.book import Book
from src.services.exceptions import DatabaseServiceError

import logging
from typing import Any


class BookServices:
    def __init__(self, book: Book, book_queries: BookQueries) -> None:
        self.book = book
        self.book_queries = book_queries

    def create_book(self) -> None:
        """
        Create a new book in the database.

        Raises:
            DatabaseServiceError: If the book creation fails.
        """
        logging.info("Attempting to create book: %s", self.book.title)
        try:
            self.book_queries.insert_book(self.book)
            logging.info("Successfully created book: %s", self.book.title)
        except Exception as e:
            logging.exception("Failed to create book")
            raise DatabaseServiceError("Failed to create book") from e

    def get_book_details(self) -> list[dict[str, Any]] | None:
        """
        Retrieve book details from the database.

        Returns:
            List of dictionaries containing book details, or None if not found.

        Raises:
            DatabaseServiceError: If the retrieval fails.
        """
        logging.info("Attempting to get book details for: %s", self.book.title)
        try:
            logging.info("Successfully retrieved book details for: %s", self.book.title)
            return self.book_queries.find_by_title(self.book)
        except Exception as e:
            logging.exception("Failed to get book details")
            raise DatabaseServiceError("Failed to get book details") from e

    def delete_book(self) -> None:
        """
        Mark a book as deleted in the database.

        Raises:
            DatabaseServiceError: If the deletion fails.
        """
        logging.info(
            "Attempting to mark: %s as deleted in the database", self.book.title
        )
        self.book.status = BookState.DELETED
        try:
            self.book_queries.update_book_status(self.book)
            logging.info(
                "Successfully marked: %s as deleted in the database", self.book.title
            )
        except Exception as e:
            logging.exception("Failed to mark book as deleted")
            raise DatabaseServiceError("Failed to mark book as deleted") from e

    def restore_book(self) -> None:
        """
        Mark a book as available in the database.

        Raises:
            DatabaseServiceError: If the restoration fails.
        """
        logging.info(
            "Attempting to mark: %s as available in the database", self.book.title
        )
        self.book.status = BookState.AVAILABLE
        try:
            logging.info(
                "Successfully marked: %s as available in the database", self.book.title
            )
            self.book_queries.update_book_status(self.book)
        except Exception as e:
            logging.exception("Failed to mark: %s as available", self.book.title)
            raise DatabaseServiceError(
                "Failed to mark: %s as available", self.book.title
            ) from e

    def set_rating(self, new_rating: int) -> None:
        """
        Update the rating of a book.

        Args:
            new_rating: The new rating value for the book.

        Raises:
            DatabaseServiceError: If the rating update fails.
        """
        logging.info("Attempting to update the rating of: %s", self.book.title)
        self.book.rating = new_rating
        try:
            logging.info("Successfully updated rating for: %s", self.book.title)
            self.book_queries.update_rating(self.book)
        except Exception as e:
            logging.exception("Failed to update book rating for: %s", self.book.title)
            raise DatabaseServiceError(
                "Failed to update book rating for: %s", self.book.title
            ) from e
