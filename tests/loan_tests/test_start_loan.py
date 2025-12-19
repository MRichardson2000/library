from data.classes.enums import LoanStatus
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_loan import auto_create_loan
from data.dataclasses.db_dataclass import DB


def test_start_loan(db_session: DB) -> None:
    auto_clear_table("loan", db_session)
    loan = auto_create_loan(db_session)
    assert loan.status == LoanStatus.BORROWED
    assert loan.inventory.quantity == 0
    auto_clear_table("loan", db_session)
