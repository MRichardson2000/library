from typing import Any
from src.services.exceptions import InvalidEmailError
from data.classes.enums import AccountState


class User:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: str,
        account_state: AccountState = AccountState.ACTIVE,
        user_id: int | None = None,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.account_state = account_state
        self._user_id = user_id

    def __repr__(self) -> str:
        return f"User(id={self._user_id}, name={self.first_name} {self.last_name}, email={self.email_address}, phone number={self.phone_number}, account state={self.account_state})"

    def update_email_address(self, new_email: str) -> None:
        if "@" not in new_email:
            raise InvalidEmailError("Email address must contain the @ symbol")
        if not new_email.endswith(".co.uk") and not new_email.endswith(".com"):
            raise InvalidEmailError("Email address must end with .com or .co.uk")
        self.email_address = new_email

    @classmethod
    def from_db_row(cls, row: dict[str, Any]) -> "User":
        return cls(
            user_id=row.get("user_id"),
            first_name=row.get("first_name", ""),
            last_name=row.get("last_name", ""),
            email_address=row.get("email_address", ""),
            phone_number=row.get("phone_number", ""),
            account_state=row.get("account_state", ""),
        )
