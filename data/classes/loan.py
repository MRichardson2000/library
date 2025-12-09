from datetime import datetime, timedelta
from data.classes.book import Book
from data.classes.user import User
from data.classes.inventory import Inventory
from typing import Optional
from src.services.data_validaters import Validaters as V


class Loan:
    def __init__(
        self,
        book: Book,
        user: User,
        inventory: Inventory,
        borrow_date: Optional[datetime] = None,
        duration_days: int = 30,
    ) -> None:
        self.book = book
        self.user = user
        self.inventory = inventory
        self._borrow_date = borrow_date or datetime.now()
        V.valid_duration_days(duration_days)
        self._due_date = self.borrow_date + timedelta(days=duration_days)
        self.return_date: Optional[datetime] = None
        V.valid_date(self._borrow_date, self._due_date)
        if self.return_date:
            V.valid_date(self.return_date)

    def __repr__(self) -> str:
        status = "Returned" if self.is_returned else "Active"
        return f"Loan (book={self.book.title}, user={self.user.first_name}, due_date={self.due_date.date()}, status={status})"

    def borrow_book(self) -> None:
        self.user.add_loan(self.book)
        self.inventory.remove_stock(1)

    def return_book(self, now: Optional[datetime] = None) -> None:
        self.return_date = now or datetime.now()
        if self.return_date > self.borrow_date + timedelta(days=30):
            pass
            # add logic here for managing fees / fee class
        self.user.remove_loan(self.book)
        self.inventory.add_stock(1)

    def extend_loan(self, extra_days: int) -> None:
        if extra_days <= 0:
            raise ValueError("Extension must be positive")
        self._due_date += timedelta(days=extra_days)

    @property
    def is_returned(self) -> bool:
        return self.return_date is not None

    @property
    def borrow_date(self) -> datetime:
        return self._borrow_date

    @property
    def is_overdue(self, grace_days: int = 0) -> bool:
        return not self.is_returned and datetime.now() > (
            self.due_date + timedelta(days=grace_days)
        )

    @property
    def due_date(self) -> datetime:
        return self._due_date
