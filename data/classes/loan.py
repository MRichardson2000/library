from datetime import datetime, timedelta
from data.classes.book import Book
from data.classes.user import User
from typing import Optional


class Loan:
    def __init__(
        self,
        book: Book,
        user: User,
        accumulated_late_fee: float = 0.0,
        loaned: bool = False,
        loan_time: datetime | None = None,
        late_fee: bool = False,
        overdue_return: bool = False,
    ) -> None:
        self.book = book
        self.user = user
        self.accumulated_late_fee = accumulated_late_fee
        self.loaned = loaned
        self.loan_time = loan_time
        self.late_fee = late_fee
        self.overdue_return = overdue_return

    def borrow_book(self, now: Optional[datetime] = None) -> None:
        if self.book.title and not self.loaned:
            self.borrow_time(now)
            self.loaned = True

    def return_book(self, now: Optional[datetime] = None) -> float:
        if self.book.title and self.loaned:
            self.loaned = False
            return self.calculate_late_fee(now)
        return 0.0

    def borrow_time(self, now: Optional[datetime] = None) -> None:
        self.loan_time = now or datetime.now()

    def calculate_late_fee(self, now: Optional[datetime] = None) -> float:
        if not self.loan_time:
            return 0.0
        now = now or datetime.now()
        if now > self.get_due_date():
            self.late_fee = True
            self.accumulated_late_fee += 2.50
            return 2.50
        return 0.0

    def extend_borrow_time(self, now: Optional[datetime] = None) -> None:
        self.borrow_time(now)

    def get_due_date(self) -> datetime:
        if not self.loan_time:
            raise ValueError("No borrow record found.")
        return self.loan_time + timedelta(days=30)

    def pay_late_fee(self) -> None:
        if self.late_fee:
            self.late_fee = False
            self.accumulated_late_fee -= 2.50

    def get_user(self) -> tuple[str, str]:
        if self.loaned:
            return self.user.first_name, self.user.last_name
        else:
            return ("no", "user")
