from __future__ import annotations
from data.classes.book import Book
from data.database.dbconn import execute_query
from data.database.models import book_insert
from src.services.base_services import BaseService
from src.services.exceptions import (
    BookAlreadyExistsError,
    DatabaseServiceError,
    BookNotFoundError,
)
from typing import Any


class BookServices(BaseService):
    def __init__(self) -> None:
        pass

    def create_book(self, book: Book) -> None:
        """
        Creates a book object in the database using the book class if the book
        doesn't already exist.

        Args:
            book (Book): a book object. The class object is in data/classes/book.py

        Returns:
            None: it just creates the object

        Raises:
            BookAlreadyExistsError: if the book already exists
            DatabaseServiceError: For any database errors
            Exception: Anything else

        Notes:
            This function will check if a book with the details passed in already
            exists. If it's found it returns BookAlreadyExistsError otherwise it creates the book
            object and adds it to the database
        """
        conditions, values = self.build_conditions(book.filters())
        verification = f"select * from book where {conditions}"
        book_check = execute_query(verification, values)
        if book_check:
            raise BookAlreadyExistsError(f"Book already exists")
        try:
            execute_query(book_insert, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to create book") from e

    def get_book_details(self, book: Book) -> list[dict[str, Any]]:
        """
        Searches the database for the details of the book passed in

        Args:
            book (Book): a Book object - the class object is in data/classes/book.py

        Returns:
            list[dict[str, Any]]: the details of the selected book

        Raises:
            BookNotFoundError: if the book is not found in the database
            DatabaseServiceError: For any database errors
            Exception: Anything else

        Notes:
            This function pulls a book and it's attributes from the database using the
            details passed in. It will return the book and it's assosciated information.

        """
        conditions, values = self.build_conditions(book.filters())
        query = f"select * from book where {conditions}"
        try:
            get_book = execute_query(query, values)
            if not get_book:
                raise BookNotFoundError("Book not found in the database")
            return get_book
        except Exception as e:
            raise DatabaseServiceError("Failed to retrieve book details") from e

    def delete_book(self, book: Book) -> None:
        """
        Attempts to delete a book from the database. It doesn't delete it, it just
        marks it as deleted in the database. It then updates the inventory table
        to show the book is no longer available by setting it to false.

        Args:
            book (Book): a Book object - the class object is in data - classes - book.py

        Returns:
            None: It marks the book as deleted and returns nothing.

        Raises:
            ValueError: If no filters are provided, if the query returns no results, or if multiple rows are found.
            BookNotFoundError: if the book isn't found in the database
            DatabaseServiceError: For any database errors
            Exception: Anything else
        Notes:
        The function first verifies the existence of the book before attempting deletion. Deletion only proceeds if exactly one matching book is found.
        The object isn't actually deleted, the deleted column is marked as True.
        This way audit history is kept.
        """
        conditions, values = self.build_conditions(book.filters())
        verification_query = f"select * from book where {conditions}"
        try:
            rows = execute_query(verification_query, values)
            if not rows:
                raise BookNotFoundError("Delete book query returned no results")
            if len(rows) > 1:
                raise ValueError("Deletion aborted due to multiple rows being found")
            delete_query = f"""
                            update book
                            set deleted = True
                            where {conditions}
                            """
            execute_query(delete_query, values)
            availability = f"""
                update inventory
                set is_available = False
                from book b
                where i.book_id = b.book_id
                and {conditions}
                """
            execute_query(availability, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to delete book") from e

    def update_book_rating(self, new_rating: int, book: Book) -> None:
        """
        Searches the database for the book passed in and attempts to update the rating.

        Args:
            new_rating: int - whatever the new rating is going to be
            book (Book): a book object - the class object is in data/classes/book.py

        Returns:
            None: it updates the rating and returns None

        Raises:
            ValueError: if the query returns no results or if multiple rows are found
            DatabaseServiceError: For any database related errors outside of our control
            Exception: Any other errors found

        Notes:
            A book is pulled from the database and then we change the rating to
            whatever is entered in.

        """
        conditions, values = self.build_conditions(book.filters())
        find_book = f"select * from book where {conditions}"
        try:
            if find_book:
                rows = execute_query(find_book, values)
                if not rows:
                    raise BookNotFoundError("Query returned no results, book not found")
                if len(rows) > 1:
                    raise ValueError("Update aborted due to multiple rows being found")
                rating = book.update_rating(new_rating)
                update_query = f"""
                                update book
                                set rating = {rating}
                                where {conditions}
                                """
                execute_query(update_query, values)
        except Exception as e:
            raise DatabaseServiceError("Failed to update book rating") from e
