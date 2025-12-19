from data.classes.book import Book
from src.services.book_services import BookServices
from data.dataclasses.db_dataclass import DB
from data.database.queries.book_queries import BookQueries


def auto_create_book(db_session: DB) -> Book:
    book = Book(
        title="test",
        author="test",
        genre="test",
        rating=1.5,
    )
    queries = BookQueries(db_session)
    service = BookServices(book, queries)
    service.create_book()
    return book
