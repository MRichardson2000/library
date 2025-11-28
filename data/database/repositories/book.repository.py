from __future__ import annotations
from data.classes.book import Book
from data.database.models import book_insert
from data.database.dbconn import execute_query
from typing import Any


class BookRepository:
    def __init__(self) -> None:
        pass

    def find(self, conditions: str, values: list[Any]) -> list[dict[str, Any]] | None:
        query = f"select * from book where {conditions}"
        return execute_query(query, values)

    def insert(self, book: Book) -> None:
        execute_query(book_insert, book)
