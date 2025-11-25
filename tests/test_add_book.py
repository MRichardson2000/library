from __future__ import annotations
from data.dbconn import execute_query, load_env
from data.dataclasses import DB
from data.classes import Book
from data.models import book_insert


def test_add_book(db: DB) -> None:
    db = load_env(testing=True)
    book = Book(1, "test", "test", "test", 3)
    execute_query(book_insert, params=book.__dict__, db_details=db)
    output = execute_query(
        """
        select *
        from library_test
        where title = 'test'
        """
    )
    assert output
    assert book.title == "test"
    assert output == book
