from data.classes.book import Book
from typing import Optional, Any


class User:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: str,
        books_loaned: list[Book] | None = None,
        user_id: Optional[int] = None,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self._email_address = email_address
        self._phone_number = phone_number
        self._books_loaned = books_loaned if books_loaned is not None else []
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"User(id={self.user_id}, name={self.first_name} {self.last_name}, loans={len(self.books_loaned)})"

    @property
    def email_address(self) -> str:
        return self._email_address

    @email_address.setter
    def email_address(self, new_email: str) -> None:
        if "@" not in new_email:
            raise ValueError("Email address must contain the @ symbol")
        self._email_address = new_email

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, new_phone_num: str) -> None:
        if not isinstance(new_phone_num, str):  # type: ignore
            raise TypeError("Phone number must be entered a string")
        self._phone_number = new_phone_num

    @property
    def books_loaned(self) -> list[Book]:
        return self._books_loaned

    def update_last_name(self, new_last_name: str) -> None:
        self.last_name = new_last_name

    def get_loaned_books_amount(self) -> int:
        return len(self._books_loaned)

    def filters(self) -> dict[str, Any]:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "phone_number": self.phone_number,
        }
