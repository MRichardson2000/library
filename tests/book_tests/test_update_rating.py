from tests.book_tests.test_add_book import test_add_book
from data.classes.book import Book


def test_update_rating() -> None:
    new_book = test_add_book()
    old_rating = new_book.rating
    new_rating = Book.update_rating(new_book, new_rating=5)
    assert new_rating
    assert old_rating != new_rating
    assert new_rating == 5
    assert isinstance(new_rating, int | float)
