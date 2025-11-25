from data.classes import Loan, User
from tests.test_add_book import test_add_book
from datetime import datetime, timedelta


def test_get_due_date() -> None:
    book = test_add_book()
    user = User(1, "user", "user", "user@user.user.user", 73849043912)
    loan = Loan(book, user)
    loan_time = datetime.now()
    loan.borrow_time(loan_time)
    due_date = loan.get_due_date()
    assert due_date > loan_time
    assert due_date == loan_time + timedelta(days=30)
