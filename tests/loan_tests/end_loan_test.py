from data.classes.enums import LoanStatus
from src.services.loan_services import LoanServices, LoanQueries
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_loan import auto_create_loan


def test_end_loan() -> None:
    auto_clear_table("loan")
    loan = auto_create_loan()
    loan_queries = LoanQueries()
    services = LoanServices(
        user=loan.user,
        loan=loan,
        loan_queries=loan_queries,
        inventory=loan.inventory,
        book=loan.book,
    )
    services.end_loan_transaction()
    assert loan.status == LoanStatus.RETURNED
    assert loan.inventory.quantity == 1
    auto_clear_table("loan")
