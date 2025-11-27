from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, Union, Any


class Library:
    def __init__(self) -> None:
        self.books: list[Book] = []
        self.users: list[User] = []
        self.inventory: list[Inventory] = []


class Book:
    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        genre: str,
        rating: Union[int, float],
    ) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating

    def __repr__(self) -> str:
        return f"Book: {self.title} by {self.author}\n Genre: {self.genre}\n Rating: {self.rating}."

    def update_rating(self, new_rating: Union[int, float]) -> None:
        if not isinstance(new_rating, (int, float)):  # type: ignore
            raise TypeError(
                f"Rating must be int or float, not {type(new_rating).__name__}"
            )
        if 1 <= new_rating <= 5:
            self.rating = new_rating
        else:
            raise ValueError("The rating needs to be between 1 and 5.")


class Loan:
    def __init__(
        self,
        book: Book,
        user: User,
        loaned: bool = False,
        loan_time: datetime | None = None,
        late_fee: bool = False,
    ) -> None:
        self.book = book
        self.user = user
        self.loaned = loaned
        self.loan_time = loan_time
        self.late_fee = late_fee

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

    def get_user(self) -> tuple[str, str]:
        if self.loaned:
            return self.user.first_name, self.user.last_name
        else:
            return ("no", "user")


class User:
    def __init__(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: int,
        books_loaned: Optional[list[Book]] = None,
    ) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.books_loaned = books_loaned if books_loaned is not None else []

    def __repr__(self) -> str:
        return f"User: {self.first_name} {self.last_name}, {len(self.books_loaned)} books loaned."

    def filters(self) -> dict[str, Any]:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
        }

    def surname_change(self, new_last_name: str) -> None:
        self.last_name = new_last_name

    def new_email(self, new_email: str) -> None:
        self.email_address = new_email

    def new_phone_number(self, new_phone_num: int) -> None:
        self.phone_number = new_phone_num

    def get_books_on_loan(self) -> int:
        return len(self.books_loaned)


class Inventory:
    def __init__(
        self,
        book_id: int,
        book_quantity: int,
        shelf_location: str,
        availability: bool,
    ) -> None:
        self.book_id = book_id
        self.book_quantity = book_quantity
        self.shelf_location = shelf_location
        self.availability = availability

    def add_stock(self, quantity: int) -> None:
        self.book_quantity += quantity

    def remove_stock(self, quantity: int) -> None:
        if not quantity <= self.book_quantity:
            self.book_quantity -= quantity

    def get_quantity(self) -> int:
        return self.book_quantity

    def get_availability(self) -> bool:
        return self.book_quantity > 0

    def update_availability(self) -> None:
        self.availability = self.book_quantity > 0

    def needs_restock(self) -> bool:
        return self.book_quantity < 2


if __name__ == "__main__":
    book = Book(1, "test", "test", "test", 4)
    book.update_rating(3)
