from data.database.dbconn import execute_query
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from tests.auto_clear_db import auto_clear_book_table
from src.services.book_services import BookServices
from typing import Any


def test_update_rating(db_session: DB) -> None:
    auto_clear_book_table()
    book = Book(
        None,
        title="test",
        author="test",
        genre="test",
        rating=3,
    )
    service = BookServices(book, db_session)
    service.create_book()
    output_before = execute_query(
        "select * from book where title = 'test'", db_details=db_session
    )
    assert output_before is not None
    row = output_before[0]
    old_rating = row["rating"]
    service.update_book_rating(5)
    assert old_rating != book.rating
    assert book.rating == 5
    assert isinstance(book.rating, int | float)
    updated_rows = execute_query(
        "select * from book where title = 'test'", db_details=db_session
    )
    assert updated_rows is not None
    updated_row: dict[str, Any] = updated_rows[0]
    assert updated_row["rating"] == book.rating == 5
    auto_clear_book_table()
