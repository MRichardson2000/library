from data.classes.book import Book
from typing import Any


class User:
    def __init__(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: int,
        books_loaned: list[Book] | None = None,
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
