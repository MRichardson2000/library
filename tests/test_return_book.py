from data.classes import Loan, User
from tests.test_add_book import test_add_book


def test_return_book() -> None:
    book = test_add_book()
    user = User(1, "user", "user", "user@user.user.user", 73849043912)
    loan = Loan(book, user)
    loan.borrow_book()
    loaned = loan.return_book()
    assert loan.loaned == False
    assert isinstance(loaned, float)
