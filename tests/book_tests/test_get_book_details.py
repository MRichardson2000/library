from __future__ import annotations
from data.database.dbconn import fetch_result
from data.classes.book import Book
from tests.auto_clear_db import auto_clear_book_table
from tests.auto_create_book import auto_create_book


def test_get_book_details(book: Book) -> None:
    auto_clear_book_table()
    auto_create_book()
    output = fetch_result("select * from book where title = 'test'")
    assert output is not None
    assert isinstance(output, list)
    assert len(output) == 1
    row = output[0]
    assert row["title"] == book.title
    assert row["author"] == book.author
    assert row["genre"] == book.genre
    assert row["rating"] == book.rating
    auto_clear_book_table()
