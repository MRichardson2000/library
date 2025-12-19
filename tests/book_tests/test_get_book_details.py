from __future__ import annotations
from data.database.dbconn import fetch_result
from data.classes.book import Book
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_book import auto_create_book
from data.dataclasses.db_dataclass import DB


def test_get_book_details(db_session: DB, book: Book) -> None:
    auto_clear_table("book", db_session)
    auto_create_book(db_session)
    output = fetch_result("select * from book where title = 'test'")
    assert output is not None
    assert isinstance(output, list)
    assert len(output) == 1
    row = output[0]
    assert row["title"] == book.title
    assert row["author"] == book.author
    assert row["genre"] == book.genre
    assert row["rating"] == book.rating
    auto_clear_table("book", db_session)
