from datetime import datetime, timedelta
from data.classes.enums import LoanStatus
from data.classes.book import Book
from data.classes.user import User
from data.classes.inventory import Inventory


class Loan:
    def __init__(
        self,
        book: Book,
        user: User,
        inventory: Inventory,
        status: LoanStatus = LoanStatus.AVAILABLE,
        loan_time: datetime | None = None,
        duration_days: int = 30,
        loan_id: int | None = None,
    ) -> None:
        self._loan_id = loan_id
        self.book = book
        self.user = user
        self.inventory = inventory
        self.status = status
        self.loan_time = loan_time or datetime.now()
        self.due_date = self.loan_time + timedelta(days=duration_days)
        self.return_date: datetime | None = None

    def __repr__(self) -> str:
        status = "Returned" if self.return_date is not None else "Active"
        return f"Loan (book={self.book.title}, user={self.user.first_name}, due_date={self.due_date.date()}, loan_status={status})"

    def borrow_book(self) -> None:
        self.loan_time = datetime.now()
        self.status = LoanStatus.BORROWED
        self.inventory.remove_stock(1)

    def return_book(self, now: datetime | None = None) -> None:
        self.return_date = now or datetime.now()
        self.status = LoanStatus.RETURNED
        self.inventory.add_stock(1)

    def extend_loan(self, extra_days: int = 30) -> None:
        if extra_days <= 0:
            raise ValueError("Extension must be positive")
        if extra_days > 30:
            raise ValueError("Extension must not exceed 30 days")
        self.due_date += timedelta(days=extra_days)

    def is_overdue(self, grace_days: int = 0) -> bool:
        """add grace days as and when necessary. Currently it's 0 as books must be returned on time"""
        return not self.return_date and datetime.now() > (
            self.due_date + timedelta(days=grace_days)
        )
