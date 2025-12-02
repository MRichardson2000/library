from __future__ import annotations
from data.database.dbconn import execute_query, load_env
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from src.services.book_services import BookServices
from tests.auto_clear_db import auto_clear_db


def test_add_book(db: DB = load_env(testing=True)) -> None:
    auto_clear_db()
    book = Book(
        None,
        title="test",
        author="test",
        genre="test",
        rating=3,
    )
    service = BookServices(book, db)
    service.create_book()
    output = execute_query("select * from book where title = 'test'", db_details=db)
    assert output is not None
    assert isinstance(output, list)  # type: ignore
    assert len(output) == 1
    row = output[0]
    assert row["title"] == book.title
    assert row["author"] == book.author
    assert row["genre"] == book.genre
    assert row["rating"] == book.rating
    execute_query("delete from book where unique_id = 1", db_details=db)
