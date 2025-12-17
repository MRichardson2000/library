# from __future__ import annotations
# from data.database.dbconn import fetch_result
# from data.classes.loan import Loan
# from data.dataclasses.db_dataclass import DB
# from src.services.loan_services import LoanServices
# from data.database.queries.loan_queries import LoanQueries
# from tests.auto_clear_db import auto_clear_loan_table
# from tests.auto_create_book import auto_create_loan


# def test_start_loan(db_session: DB, loan: Loan) -> None:
#     auto_clear_loan_table()
#     auto_create_loan()
#     output_before = fetch_result("select * from loan where x = 'x'")
#     assert output_before is not None
#     queries = LoanQueries(db_session)
#     service = LoanServices(loan, queries)
#     service.start_loan_transaction()
