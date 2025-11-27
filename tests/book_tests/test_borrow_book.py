from data.classes.loan import Loan
from data.classes.user import User
from tests.book_tests.test_add_book import test_add_book


def test_borrow_book() -> None:
    book = test_add_book()
    user = User(1, "user", "user", "user@user.user.user", 73849043912)
    loan = Loan(book, user)
    loan.borrow_book()
    assert loan.loaned == True
    assert user.first_name == "user"
