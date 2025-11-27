from data.classes.loan import Loan
from data.classes.user import User
from tests.book_tests.test_add_book import test_add_book
from datetime import datetime, timedelta


def test_extend_borrow_time() -> None:
    book = test_add_book()
    user = User(1, "user", "user", "user@user.user.user", 73849043912)
    loan = Loan(book, user)
    loan.borrow_book()
    extension_time = loan.extend_borrow_time(now=datetime.now() + timedelta(days=30))
    assert loan.loaned == True
    assert loan.late_fee == False
    assert extension_time == datetime.now() + timedelta(days=30)
