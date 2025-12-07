from src.services.exceptions import DatabaseServiceError
from src.services.base_services import BaseService
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from data.database.sql_models import book_insert
from data.database.dbconn import execute_query
from typing import Any


class BookRepository:
    def __init__(self, db_details: DB) -> None:
        self.db_details = db_details

    def find_by_filters(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        conditions, params = BaseService.build_conditions(filters)
        query = f"select * from book where {conditions} and deleted = false"
        result = execute_query(query, params, self.db_details) or []
        return result

    def insert(self, book: Book) -> None:
        try:
            execute_query(
                book_insert,
                {
                    "title": book.title,
                    "author": book.author,
                    "genre": book.genre,
                    "rating": book.rating,
                },
                self.db_details,
            )
        except Exception as e:
            raise DatabaseServiceError("Failed to insert book") from e
