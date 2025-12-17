from data.database.queries.base_queries import Queries
from data.database.sql_models import book_insert
from data.database.dbconn import fetch_result, execute_query
from typing import Any


class BookQueries(Queries):
    def find_by_title(self) -> list[dict[str, Any]] | None:
        rows = fetch_result(
            "select * from book where title = :title", {"title": self.book.title}
        )
        if rows:
            return rows

    def update_book_status(self) -> None:
        rows = self.find_by_title()
        if rows and len(rows) == 1:
            execute_query(
                "update book set status = :status", {"status": self.book.status}
            )

    def update_rating(self) -> None:
        rows = self.find_by_title()
        if rows and len(rows) == 1:
            execute_query(
                "update book set rating = :rating", {"rating": self.book.rating}
            )

    def insert_book(self) -> None:
        rows = self.find_by_title()
        if not rows:
            execute_query(book_insert, self.book.to_dict())
