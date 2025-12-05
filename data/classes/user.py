from data.classes.book import Book
from typing import Optional


class User:
    def __init__(
        self,
        user_id: Optional[int],
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: int,
        books_loaned: list[Book] | None = None,
    ) -> None:
        self._user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self._email_address = email_address
        self._phone_number = phone_number
        self._books_loaned = books_loaned if books_loaned is not None else []

    def __repr__(self) -> str:
        return f"User: {self.first_name} {self.last_name}, {len(self.books_loaned)} books loaned."

    @property
    def user_id(self) -> Optional[int]:
        return self._user_id

    @property
    def email_address(self) -> str:
        return self._email_address

    @email_address.setter
    def email_address(self, new_email: str) -> None:
        if "@" not in new_email:
            raise ValueError("Email address must contain the @ symbol")
        self._email_address = new_email

    @property
    def phone_number(self) -> int:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, new_phone_num: int) -> None:
        if not isinstance(new_phone_num, int):  # type: ignore
            raise TypeError("Phone number must be entered as an integer")
        self._phone_number = new_phone_num

    @property
    def books_loaned(self) -> list[Book]:
        return self._books_loaned

    def update_last_name(self, new_last_name: str) -> None:
        self.last_name = new_last_name

    def get_loaned_books_amount(self) -> int:
        return len(self._books_loaned)
