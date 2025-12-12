from data.classes.book import Book
from typing import Optional, Any


class User:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: str,
        deleted: bool = False,
        user_id: Optional[int] = None,
    ) -> None:
        self._first_name = first_name
        self._last_name = last_name
        self._email_address = email_address
        self._phone_number = phone_number
        self.deleted = deleted
        self._user_id = user_id

    def __repr__(self) -> str:
        return f"User(id={self.user_id}, name={self.first_name} {self.last_name}, loans={len(self.books_loaned)})"

    @property
    def user_id(self) -> int | None:
        return self._user_id

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name: str) -> None:
        self._last_name = new_last_name

    @user_id.setter
    def user_id(self, value: int) -> None:
        self._user_id = value

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
        self._phone_number = new_phone_num

    @property
    def books_loaned(self) -> list[Book]:
        return self._books_loaned

    @books_loaned.setter
    def books_loaned(self, new_list: list[Book]) -> None:
        self._books_loaned = new_list

    def update_last_name(self, new_last_name: str) -> None:
        self._last_name = new_last_name

    def get_loaned_books_amount(self) -> int:
        return len(self._books_loaned)

    def filters(self) -> dict[str, Any]:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "phone_number": self.phone_number,
        }

    @classmethod
    def from_db_rows(cls, row: dict[str, Any]) -> "User":
        return cls(
            user_id=row.get("user_id"),
            first_name=row.get("first_name", ""),
            last_name=row.get("last_name", ""),
            email_address=row.get("email_address", ""),
            phone_number=row.get("phone_number", ""),
            deleted=row.get("deleted", False),
        )

    """
    example use case of the above

        row = {
        "user_id": 1,
        "first_name": "test",
        "last_name": "test",
        "email_address": "test@test.test.test",
        "phone_number": "0123456789",
        "deleted": False,
    }

    user = User.from_db_row(row)
    print(user) 
    """
