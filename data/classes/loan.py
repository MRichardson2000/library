from datetime import datetime, timedelta
from data.classes.book import Book
from data.classes.user import User
from typing import Optional


class Loan:
    def __init__(
        self,
        book: Book,
        user: User,
        borrow_date: Optional[datetime] = None,
        duration_days: int = 30,
    ) -> None:
        self.book = book
        self.user = user
        self.borrow_date = borrow_date or datetime.now()
        self.due_date = self.borrow_date + timedelta(days=duration_days)
        self.return_date: Optional[datetime] = None

    def return_book(self, now: Optional[datetime] = None) -> None:
        self.return_date = now or datetime.now()

    def extend_loan(self, extra_days: int) -> None:
        self.due_date += timedelta(days=extra_days)

    @property
    def is_returned(self) -> bool:
        return self.return_date is not None

    @property
    def is_overdue(self) -> bool:
        return not self.is_returned and datetime.now() > self.due_date

    def get_due_date(self) -> datetime:
        return self.due_date
