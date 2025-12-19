from __future__ import annotations
from data.database.dbconn import fetch_result
from data.classes.book import Book
from src.services.book_services import BookServices
from data.database.queries.book_queries import BookQueries
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_book import auto_create_book
from data.dataclasses.db_dataclass import DB


def test_delete_book(book: Book, db_session: DB) -> None:
    auto_clear_table("book", db_session)
    auto_create_book(db_session)
    output_before = fetch_result("select * from book where title = 'test'")
    assert output_before is not None
    queries = BookQueries(db_session)
    service = BookServices(book, queries)
    service.delete_book()
    status = fetch_result("select status from book where title = 'test")
    assert status[0]["status"] == "Deleted"
    auto_clear_table("book", db_session)
