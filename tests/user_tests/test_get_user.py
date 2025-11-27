from data.classes.loan import Loan
from data.classes.user import User
from tests.book_tests.test_add_book import test_add_book
from datetime import datetime


def test_get_user() -> None:
    book = test_add_book()
    user = User(1, "user", "user", "user@user.user.user", 73849043912)
    loan = Loan(book, user)
    loan.borrow_book(now=datetime.now())
    get_user = loan.get_user()
    assert get_user == (user.first_name, user.last_name)
