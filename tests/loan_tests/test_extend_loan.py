from datetime import datetime, timedelta
from src.services.loan_services import LoanServices, LoanQueries
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_loan import auto_create_loan
from data.dataclasses.db_dataclass import DB


def test_extend_lon(db_session: DB) -> None:
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
    old_due_date = loan.due_date
    services.extend_loan_transaction()
    assert old_due_date != loan.due_date
    remaining = loan.due_date - datetime.now()
    assert remaining >= timedelta(days=30)
    assert loan.due_date == old_due_date + timedelta(days=30)
    auto_clear_table("loan", db_session)
