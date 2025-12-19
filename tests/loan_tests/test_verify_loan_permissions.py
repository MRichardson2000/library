from src.services.loan_services import LoanServices, LoanQueries
from tests.auto_clear_db import auto_clear_table
from tests.auto_create_loan import auto_create_loan
from data.dataclasses.db_dataclass import DB


def test_verification_allows_within_limit(db_session: DB) -> None:
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
    result = services.verify_loan_permissions()
    assert result is False
    auto_clear_table("loan", db_session)


def test_verification_blocks_over_limit(db_session: DB) -> None:
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
    for _ in range(6):
        auto_create_loan(db_session)
    result = services.verify_loan_permissions()
    assert result is True
    auto_clear_table("loan", db_session)
