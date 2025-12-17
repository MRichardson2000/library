from data.classes.book import Book
from data.classes.user import User
from data.classes.loan import Loan
from data.classes.inventory import Inventory


class Queries:
    def __init__(
        self, book: Book, user: User, loan: Loan, inventory: Inventory
    ) -> None:
        self.book = book
        self.user = user
        self.loan = loan
        self.inventory = inventory
