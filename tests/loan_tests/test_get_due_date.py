from datetime import datetime
from src.services.loan_services import LoanServices, LoanQueries
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_loan import auto_create_loan
from data.dataclasses.db_dataclass import DB


def test_due_date_retrieval(db_session: DB) -> None:
    auto_clear_table("loan", db_session)
    loan = auto_create_loan(db_session)
    loan_queries = LoanQueries(db_session)
    services = LoanServices(
        user=loan.user,
        loan=loan,
        loan_queries=loan_queries,
        inventory=loan.inventory,
        book=loan.book,
    )
    due_date = services.get_due_date()
    assert due_date is not None
    assert due_date == loan.due_date
    assert due_date > datetime.now()
    auto_clear_table("loan", db_session)
