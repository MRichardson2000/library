from data.classes import Loan, User
from tests.test_add_book import test_add_book
from datetime import datetime
import time


def test_extend_borrow_time() -> None:
    book = test_add_book()
    user = User(1, "user", "user", "user@user.user.user", 73849043912)
    loan = Loan(book, user, expected_return=datetime.now())
    loan.borrow_book()
    now = datetime.now()
    time.sleep(300)
    loan.extend_borrow_time()
    extension_time = datetime.now()
    assert extension_time > now
    assert extension_time != now
    assert loan.loaned == True
    assert loan.late_fee == False
