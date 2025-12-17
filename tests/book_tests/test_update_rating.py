from data.database.dbconn import execute_query, fetch_result
from data.classes.book import Book
from src.services.book_services import BookServices
from data.dataclasses.db_dataclass import DB
from data.database.queries.book_queries import BookQueries
from tests.auto_clear_db import auto_clear_book_table
from tests.auto_create_book import auto_create_book
from typing import Any


def test_update_rating(book: Book, db_session: DB) -> None:
    auto_clear_book_table()
    auto_create_book()
    output_before = fetch_result("select * from book where title = 'test'")
    assert output_before is not None
    row = output_before[0]
    old_rating = row["rating"]
    queries = BookQueries(db_session)
    service = BookServices(book, queries)
    service.set_rating(5)
    assert old_rating != book.rating
    assert book.rating == 5
    assert isinstance(book.rating, float)
    updated_rows = execute_query("select * from book where title = 'test'")
    assert updated_rows is not None
    updated_row: dict[str, Any] = updated_rows[0]
    assert updated_row["rating"] == book.rating == 5
    auto_clear_book_table()
