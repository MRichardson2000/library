from data.classes.book import Book
from typing import Any


class Inventory:
    def __init__(self, book: Book, quantity: int, restock_threshold: int = 2) -> None:
        if not isinstance(quantity, int):  # type: ignore
            raise TypeError("Quantity must be an integer")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.book = book
        self._quantity = quantity
        self._restock_threshold = restock_threshold

    def __repr__(self) -> str:
        return f"Inventory (book={self.book.title}, quantity={self.quantity})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "book_id": self.book.book_id,
            "title": self.book.title,
            "quantity": self.quantity,
        }

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, new_quantity: int) -> None:
        if not isinstance(new_quantity, int):  # type: ignore
            raise TypeError("New Quantity must be an integer")
        if new_quantity < 0:
            raise ValueError("New Quantity cannot be negative")
        self._quantity = new_quantity

    def add_stock(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("amount must be greater than 0")
        self._quantity += amount

    def remove_stock(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("stock removal must not be 0 or less")
        if amount > self._quantity:
            raise ValueError("Not enough stock to remove")
        self._quantity -= amount

    @property
    def availability(self) -> bool:
        return self._quantity > 0

    def needs_restock(self) -> bool:
        return self._quantity < self._restock_threshold
