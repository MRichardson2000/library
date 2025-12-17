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
        logging.info("Attempting to create book: %s", self.book.title)
        try:
            self.book_queries.insert_book()
        except Exception as e:
            logging.exception("Failed to create book")
            raise DatabaseServiceError("Failed to create book") from e

    def get_book_details(self) -> list[dict[str, Any]] | None:
        try:
            rows = self.book_queries.find_by_title()
            return rows
        except Exception as e:
            raise DatabaseServiceError("Failed to get book details") from e

    def delete_book(self) -> None:
        self.book.status = BookState.DELETED
        try:
            self.book_queries.update_book_status()
        except Exception as e:
            raise DatabaseServiceError("Failed to mark book as deleted") from e

    def restore_book(self) -> None:
        self.book.status = BookState.AVAILABLE
        try:
            self.book_queries.update_book_status()
        except Exception as e:
            raise DatabaseServiceError("Failed to mark book as restored") from e

    def set_rating(self, new_rating: int) -> None:
        self.book.rating = new_rating
        try:
            self.book_queries.update_rating()
        except Exception as e:
            raise DatabaseServiceError("Failed to update book rating") from e
