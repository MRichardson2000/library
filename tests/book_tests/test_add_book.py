from __future__ import annotations
from data.database.dbconn import execute_query, load_env
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from data.database.models import book_insert


def test_add_book(db: DB = load_env(testing=True)) -> Book:
    execute_query("ALTER SEQUENCE library_test_unique_id_seq RESTART WITH 1;")
    book = Book(1, "test", "test", "test", 3)
    execute_query(book_insert, params=book.__dict__, db_details=db)
    output = execute_query(
        """
        select *
        from book
        where title = 'test'
        """
    )
    assert output
    assert book.title == "test"
    assert output == book
    return book
