from data.classes.book import Book
from data.database.sql_models import book_insert
from data.dataclasses.db_dataclass import DB
from data.database.dbconn import fetch_result, execute_query
from typing import Any


class BookQueries:
    def __init__(self, db_session: DB) -> None:
        self.db_session = db_session

    def find_by_title(self, book: Book) -> list[dict[str, Any]] | None:
        rows = fetch_result(
            "select * from book where title = :title", {"title": book.title}
        )
        if rows:
            return rows

    def update_book_status(self, book: Book) -> None:
        rows = self.find_by_title(book)
        if rows and len(rows) == 1:
            execute_query(
                "update book set status = :status where title = :title",
                {"status": book.status, "title": book.title},
            )

    def update_rating(self, book: Book) -> None:
        rows = self.find_by_title(book)
        if rows and len(rows) == 1:
            execute_query(
                "update book set rating = :rating where title = :title",
                {"rating": book.rating, "title": book.title},
            )

    def insert_book(self, book: Book) -> None:
        rows = self.find_by_title(book)
        if not rows:
            execute_query(book_insert, book.to_dict())
