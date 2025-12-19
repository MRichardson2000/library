from data.classes.loan import Loan
from data.dataclasses.db_dataclass import DB
from data.classes.inventory import Inventory
from tests.auto_create_book import auto_create_book
from tests.auto_create_user import auto_create_user


def auto_create_loan(db_session: DB) -> Loan:
    book = auto_create_book(db_session)
    user = auto_create_user(db_session)
    inventory = Inventory(book, 1)
    loan = Loan(book, user, inventory)
    loan = Loan(book, user, inventory)
    loan.borrow_book()
    return loan
