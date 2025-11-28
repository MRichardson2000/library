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

    def get_book_details(self, book: Book) -> list[dict[str, Any]] | None:
        """
        Searches the database for the details of the book passed in

        Args:
            book (Book): a Book object - the class object is in data/classes/book.py

        Returns:
            list of dictionary's containing a string and then Any

        Raises:
            Exception: handles any errors outside of our control such as database
            errors

        Notes:
            This function uses a dictionary comprehension to create a new dictionary
            which filters out None values. We then pull from the database using the
            details passed in. It will return the book and it's assosciated information.

        """
        try:
            filters: dict[str, Any] = book.filters()
            filters = {k: v for k, v in filters.items() if v is not None}
            if not filters:
                raise ValueError(
                    "You need to pass in at least one value to get the details of a book"
                )
            conditions = " and ".join([f"{k} = %s" for k in filters.keys()])
            book_details = f"select * from book where {conditions}"
            values = tuple(filters.values())
            return execute_query(book_details, values)
        except Exception:
            raise

    def delete_book(self, book: Book) -> bool:
        """
        Attempts to delete a book from the database. It doesn't delete it, it just
        marks it as deleted in the database

        Args:
            book (Book): a Book object - the class object is in data - classes - book.py

        Returns:
            bool: True if the book was successfully deleted otherwise false. Raises
            an error if no matching book is found or if multiple matches exist.

        Raises:
            ValueError: If no filters are provided, if the query returns no results, or if multiple rows are found.
            Exception: For unexpected errors outside of our control such as database related issues

        Notes:
        A dictionary comprehension is used to remove None values from the filters before building the query.
        The function first verifies the existence of the book before attempting deletion.
        Deletion only proceeds if exactly one matching book is found.
        """
        try:
            filters: dict[str, Any] = book.filters()
            filters = {k: v for k, v in filters.items() if v is not None}
            if not filters:
                raise ValueError("At least one filter must be provided")
            conditions = " and ".join([f"{k} = %s" for k in filters.keys()])
            values = list(filters.values())
            deletion_verification = f"select * from book where {conditions}"
            rows = execute_query(deletion_verification, values)
            if not rows:
                raise ValueError("Delete book query returned no results")
            if len(rows) == 1:
                delete_query = f"""
                                update book
                                set deleted = True
                                where (
                                    select * from book where {conditions}
                                )
                                """
                execute_query(delete_query, values)
                return True
            else:
                raise ValueError("Deletion aborted due to multiple rows being found")
        except Exception:
            raise
