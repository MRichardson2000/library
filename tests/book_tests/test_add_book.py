from __future__ import annotations
from data.database.dbconn import execute_query
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from src.services.book_services import BookServices
from src.services.base_services import BookQueryExecutor, DefaultFilterBuilder
from tests.auto_clear_db import auto_clear_book_table


def test_add_book(db_session: DB) -> None:
    auto_clear_book_table()
    book = Book(
        None,
        title="test",
        author="test",
        genre="test",
        rating=3,
    )
    executor = BookQueryExecutor(db_session)
    filters = DefaultFilterBuilder(db_session)
    service = BookServices(book, executor, filters)
    service.create_book()
    output = execute_query(
        "select * from book where title = 'test'", db_details=db_session
    )
    assert output is not None
    assert isinstance(output, list)
    assert len(output) == 1
    row = output[0]
    assert row["title"] == book.title
    assert row["author"] == book.author
    assert row["genre"] == book.genre
    assert row["rating"] == book.rating
    auto_clear_book_table()
