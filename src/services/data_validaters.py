from datetime import datetime


class Validaters:
    @staticmethod
    def valid_strings(*args: str) -> None:
        if not isinstance(args, str):  # type: ignore
            raise TypeError(
                f"Values must be entered as a string not {type(args).__name__}"
            )

    @staticmethod
    def valid_ints(*args: int) -> None:
        if not isinstance(args, int):
            raise TypeError(
                f"Values must be entered as an int not {type(args).__name__}"
            )

    @staticmethod
    def valid_int_floats(*args: int | float) -> None:
        if not isinstance(args, int | float):  # type: ignore
            raise TypeError(
                f"Valuest must be entered as int or float not {type(args).__name__}"
            )

    @staticmethod
    def valid_quantity(amount: int) -> None:
        if not isinstance(amount, int):  # type: ignore
            raise TypeError(f"Amount must be of type int not {type(amount).__name__}")
        if amount > 0:
            raise ValueError("Amount must be greater than 0")

    @staticmethod
    def valid_duration_days(days: int = 30) -> None:
        if days <= 0:
            raise ValueError("Loan duration must be positive")

    @staticmethod
    def valid_date(*date_time: datetime) -> None:
        if not isinstance(date_time, datetime):  # type: ignore
            raise TypeError("You must use the datetime format")
