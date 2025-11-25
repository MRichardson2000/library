from data.classes import Loan, User
from tests.test_add_book import test_add_book
from datetime import datetime, timedelta


def test_pay_late_fee() -> None:
    book = test_add_book()
    user = User(1, "user", "user", "user@user.user.user", 73849043912)
    loan = Loan(book, user)
    borrow_time = datetime.now()
    loan.borrow_time(now=borrow_time)
    return_date = loan.get_due_date()
    assert loan.late_fee == True
    assert loan.calculate_late_fee() == 2.50
    if return_date == borrow_time + timedelta(days=30):
        loan.pay_late_fee()
    assert loan.late_fee == False
