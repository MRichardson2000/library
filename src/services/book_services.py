from __future__ import annotations
from data.classes.book import Book
from data.database.sql_models import book_insert
from data.classes.book import Book
from src.services.base_services import BookQueryExecutor, FilterBuilder
from src.services.exceptions import (
    BookAlreadyExistsError,
    DatabaseServiceError,
    BookNotFoundError,
)
import logging
from typing import Any


class BookServices:
    def __init__(
        self, book: Book, executor: BookQueryExecutor, filters: FilterBuilder
    ) -> None:
        self.book = book
        self.executor = executor
        self.filters = filters

    def create_book(self) -> None:
        """
        Create a new book record in the database if it does not already exist.

        Raises:
            BookAlreadyExistsError: If a book with the same details exists.
            DatabaseServiceError: If a database operation fails.
        """
        logging.info("Attempting to create book: %s", self.book.title)
        conditions, values = self.filters.build_conditions(self.book.filters())
        query = f"select * from book where {conditions}"
        try:
            book_check = self.executor.execute(query, values)
            if book_check:
                book_msg = "Book Already exists:"
                logging.warning(book_msg, "%s", self.book.title)
                raise BookAlreadyExistsError(book_msg)
            rows = self.executor.execute(book_insert, values)
            if not rows or "book_id" not in rows[0]:
                book_id_msg = "Insert failed for book:"
                logging.error(
                    "%s, %s, %s, due to a book_id not being returned",
                    book_id_msg,
                    "%s",
                    self.book.title,
                )
                raise DatabaseServiceError(book_id_msg)
            self.book.book_id = rows[0]["book_id"]
            logging.info("Book created successfully with id: %s", self.book.book_id)
        except Exception as e:
            logging.exception("Failed to create book")
            raise DatabaseServiceError("Failed to create book") from e

        """
        example use case

        db = DB("user", "pass", "host", "5432", "library")
        executor = BookQueryExecutor(db)
        filters = DefaultFilterBuilder(db)
        service = BookServices(book, executor, filters)
        """

    def get_book_details(self) -> dict[str, Any]:
        """
        Retrieve details of the current book from the database.

        Returns:
            list[dict[str, Any]]: A list of matching book records.

        Raises:
            BookNotFoundError: If no book is found.
            DatabaseServiceError: If a database operation fails.
        """
        logging.info("Attempting to pull out book details from the database")
        conditions, values = self.filters.build_conditions(self.book.filters())
        query = f"select * from book where {conditions}"
        try:
            get_book = self.executor.execute(query, values)
            if not get_book:
                logging.warning("Failed to find book in the database")
                raise BookNotFoundError("Book not found in the database")
            return get_book[0]
        except Exception as e:
            logging.exception("Failed to retrieve book details")
            raise DatabaseServiceError("Failed to retrieve book details") from e

    def delete_book(self) -> None:
        """
        Mark the current book as deleted and update inventory availability.

        Raises:
            ValueError: If no filters are provided, no results are found, or multiple matches exist.
            BookNotFoundError: If the book is not found in the database.
            DatabaseServiceError: If a database operation fails.
        """
        logging.info("Attempting to mark a book as deleted in the database")
        conditions, values = self.filters.build_conditions(self.book.filters())
        verification_query = f"select * from book where {conditions}"
        try:
            rows = self.executor.execute(verification_query, values)
            if not rows:
                row_msg = "Delete book query returned no results"
                logging.warning(row_msg)
                raise BookNotFoundError(row_msg)
            if len(rows) > 1:
                len_msg = "Deletion aborted due to multiple rows being found"
                logging.warning(len_msg)
                raise ValueError(len_msg)
            delete_query = f"""
                            update book
                            set deleted = True
                            where {conditions}
                            """
            self.executor.execute(delete_query, values)
            availability = f"""
                update inventory i
                set is_available = False
                from book b
                where i.book_id = b.book_id
                and {conditions}
                """
            self.executor.execute(availability, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to delete book") from e

    def update_book_rating(self, new_rating: int) -> None:
        """
        Update the rating of the current book in the database.

        Args:
            new_rating (int): The new rating value.

        Raises:
            ValueError: If no results are found or multiple matches exist.
            DatabaseServiceError: If a database operation fails.
        """
        conditions, values = self.filters.build_conditions(self.book.id_filter())
        find_book = f"select * from book where {conditions}"
        try:
            rows = self.executor.execute(find_book, values)
            if not rows:
                raise BookNotFoundError("Query returned no results, book not found")
            if len(rows) > 1:
                raise ValueError("Update aborted due to multiple rows being found")
            self.book.rating = new_rating
            update_query = f"""
                            update book
                            set rating = :rating
                            where {conditions}
                            """
            values["rating"] = new_rating
            self.executor.execute(update_query, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to update book rating") from e
