# from data.classes.loan import Loan
# from src.services.loan_services import LoanServices
# from data.dataclasses.db_dataclass import DB
# from data.database.queries.loan_queries import LoanQueries
# from tests.auto_create_book import auto_create_book
# from data.database.dbconn import load_env


# def auto_create_loan(db_session: DB = load_env(testing=True)) -> Loan:
#     loan = Loan(
#         book=auto_create_book(),

#     )
#     queries = LoanQueries(db_session)
#     service = LoanServices(loan, queries)
#     service.start_loan_transaction()
#     return loan
