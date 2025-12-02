from __future__ import annotations
from data.database.dbconn import execute_query, load_env
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from tests.auto_clear_db import auto_clear_db
from src.services.book_services import BookServices


def test_update_rating(db: DB = load_env(testing=True)) -> None:
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
    output_before = execute_query(
        "select * from book where title = 'test'", db_details=db
    )
    assert output_before is not None
    row = output_before[0]
    old_rating = row["rating"]
    Book.update_rating(book, new_rating=5)
    assert old_rating != book.rating
    assert book.rating == 5
    assert isinstance(book.rating, int | float)
    service.update_book_rating(5)
    updated_row = execute_query("select * from book where book_id = 1", db_details=db)[
        0
    ]
    assert updated_row["rating"] == book.rating == 5
    execute_query("delete from book where unique_id = 1", db_details=db)
