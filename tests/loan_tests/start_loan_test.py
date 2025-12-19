from data.classes.enums import LoanStatus
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_loan import auto_create_loan


def test_start_loan() -> None:
    auto_clear_table("loan")
    loan = auto_create_loan()
    assert loan.status == LoanStatus.BORROWED
    assert loan.inventory.quantity == 0
    auto_clear_table("loan")
