from data.classes import Loan, User
from tests.test_add_book import test_add_book
from datetime import datetime, timedelta


def test_get_due_date() -> None:
    book = test_add_book()
    user = User(1, "user", "user", "user@user.user.user", 73849043912)
    loan = Loan(book, user)
    loan.borrow_time()
    due_date = loan.get_due_date()
    assert due_date
    assert due_date == datetime.now() + timedelta(days=30)
