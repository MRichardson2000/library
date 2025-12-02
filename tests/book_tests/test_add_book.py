from __future__ import annotations
from data.database.dbconn import execute_query, load_env
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from src.services.book_services import BookServices


def test_add_book(db: DB = load_env(testing=True)):
    execute_query("ALTER SEQUENCE book_unique_id_seq RESTART WITH 1;")
    book = Book(
        book_id=1,
        title="test",
        author="test",
        genre="test",
        rating=3,
        deleted=False
    )
    filters = book.filters()
    book_dict = {"title": "test", "author": "test", "genre": "test", "rating": 3}
    filters = Book.filters(**book_dict)
    output = execute_query(
        """
        select *
        from book
        where title = 'test'
        """, db_details=db
    )
    assert output is not None
    assert isinstance(output, list) # type: ignore
    assert len(output) == 1
    row = output[0]
    assert row["title"] == book.title
    assert row["author"] == book.author
    assert row["genre"] == book.genre
    assert row["rating"] == book.rating
    execute_query("delete from book where unique_id = 1", db_details=db)
    
