from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DB:
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str


@dataclass(frozen=True)
class User:
    first_name: str
    last_name: str
    email_address: str
    phone_number: int | None = None
    books_loaned: int = 0

    def to_dict(self, include_phone: bool = True, include_books: bool = True):
        user_dict = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
        }
        if include_phone and self.phone_number is not None:
            user_dict["phone_number"] = self.phone_number


def create_user(first_name: str, last_name: str) -> None:
    pass
