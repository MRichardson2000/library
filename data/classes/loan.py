from datetime import datetime, timedelta
from data.classes.loan_status import LoanStatus
from data.classes.book import Book
from data.classes.user import User
from data.classes.inventory import Inventory
from typing import Optional, Any
from enum import Enum


class Loan:
    def __init__(
        self,
        book: Book,
        user: User,
        inventory: Inventory,
        status: LoanStatus = LoanStatus.AVAILABLE,
        loan_time: Optional[datetime] = None,
        duration_days: int = 30,
        loan_id: Optional[int] = None,
    ) -> None:
        self.loan_id = loan_id
        self.book = book
        self.user = user
        self.inventory = inventory
        self._status = status
        self.inventory_id = inventory.inventory_id
        self._loan_time = loan_time or datetime.now()
        self._due_date = self.loan_time + timedelta(days=duration_days)
        self.return_date: Optional[datetime] = None

    def __repr__(self) -> str:
        status = "Returned" if self.is_returned else "Active"
        return f"Loan (book={self.book.title}, user={self.user.first_name}, due_date={self.due_date.date()}, status={status})"

    def borrow_book(self) -> None:
        self.inventory.remove_stock(1)

    def return_book(self, now: Optional[datetime] = None) -> None:
        self.return_date = now or datetime.now()
        self.status = "Available"
        if self.return_date > self.loan_time + timedelta(days=30):
            pass
            # add logic here for managing fees later / fee class

        self.inventory.add_stock(1)

    def extend_loan(self, extra_days: int) -> None:
        if extra_days <= 0:
            raise ValueError("Extension must be positive")
        self._due_date += timedelta(days=extra_days)

    @property
    def is_returned(self) -> bool:
        return self.return_date is not None

    @property
    def loan_time(self) -> datetime:
        return self._loan_time

    @loan_time.setter
    def loan_time(self, new_datetime: datetime = datetime.now()):
        self._loan_time = new_datetime
        return self._loan_time

    @property
    def is_overdue(self, grace_days: int = 0) -> bool:
        """add grace days as and when necessary. Currently it's 0 as books must be returned on time"""
        return not self.is_returned and datetime.now() > (
            self.due_date + timedelta(days=grace_days)
        )

    @property
    def due_date(self) -> datetime:
        return self._due_date

    def filters(self) -> dict[str, Any]:
        return {
            "book_id": self.book.book_id,
            "user_id": self.user.user_id,
            "inventory_id": self.inventory.inventory_id,
            "loan_time": self.loan_time,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "status": self.status,
        }

    @property
    def status(self) -> Enum:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        allowed = {"Available", "Borrowed", "Returned", "Overdue"}
        if value not in allowed:
            raise ValueError(f"Value must be one of the following: {allowed}")
