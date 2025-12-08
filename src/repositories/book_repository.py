from src.services.exceptions import DatabaseServiceError
from src.services.base_services import DefaultFilterBuilder, QueryExecutor
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from data.database.sql_models import book_insert
from typing import Any


class BookRepository:
    def __init__(self, db: DB) -> None:
        self.filters = DefaultFilterBuilder(db)
        self.executor = QueryExecutor(db)
        self.db = db

    def find_by_filters(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        conditions, params = self.filters.build_conditions(filters)
        query = f"select * from book where {conditions} and deleted = false"
        result = self.executor.execute(query, params) or []
        return result

    def insert(self, book: Book) -> None:
        try:
            self.executor.execute(
                book_insert,
                {
                    "title": book.title,
                    "author": book.author,
                    "genre": book.genre,
                    "rating": book.rating,
                },
            )
        except Exception as e:
            raise DatabaseServiceError("Failed to insert book") from e
