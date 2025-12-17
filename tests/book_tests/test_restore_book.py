from __future__ import annotations
from data.database.dbconn import fetch_result
from data.classes.book import Book
from data.dataclasses.db_dataclass import DB
from src.services.book_services import BookServices
from data.database.queries.book_queries import BookQueries
from tests.auto_clear_db import auto_clear_book_table
from tests.auto_create_book import auto_create_book


def test_restore_book(db_session: DB, book: Book) -> None:
    auto_clear_book_table()
    auto_create_book()
    output_before = fetch_result("select * from book where title = 'test'")
    assert output_before is not None
    queries = BookQueries(db_session)
    service = BookServices(book, queries)
    service.restore_book()
    status = fetch_result("select status from book where title = 'test")
    assert status[0]["status"] == "Available"
