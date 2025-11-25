from data.classes import Loan, User
from tests.test_add_book import test_add_book
from datetime import datetime


def test_borrow_book() -> None:
    book = test_add_book()
    user = User(1, "user", "user", "user@user.user.user", 73849043912)
    loan = Loan(book, user, expected_return=datetime.now())
    loan.borrow_book()
    assert loan.loaned == True
    assert user.first_name == "user"
