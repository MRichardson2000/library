from data.classes.book import Book
from src.services.data_validaters import Validaters as V
from typing import Any


class Inventory:
    def __init__(
        self,
        book: Book,
        quantity: int,
        restock_threshold: int = 2,
    ) -> None:
        self.book = book
        self._quantity = quantity
        V.valid_quantity(quantity)
        self._restock_threshold = restock_threshold

    def __repr__(self) -> str:
        return f"Inventory (book={self.book.title}, quantity={self.quantity}, current restock_threshold={self.restock_threshold})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Inventory):
            return NotImplemented
        return self.book == other.book

    def __hash__(self) -> int:
        return hash(self.book)

    def filters(self) -> dict[str, Any]:
        return {
            "book_id": self.book.book_id,
            "quantity_available": self.quantity,
            "restock_threshold": self.restock_threshold,
        }

    @property
    def restock_threshold(self) -> int:
        return self._restock_threshold

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, new_quantity: int) -> None:
        V.valid_quantity(new_quantity)
        self._quantity = new_quantity

    def add_stock(self, amount: int) -> None:
        V.valid_quantity(amount)
        self._quantity += amount

    def remove_stock(self, amount: int) -> None:
        V.valid_quantity(amount)
        self._quantity -= amount

    @property
    def availability(self) -> bool:
        return self._quantity > 0

    def needs_restock(self) -> bool:
        return self._quantity < self._restock_threshold

    @classmethod
    def from_db_rows(cls, row: dict[str, Any]) -> "Inventory":
        book = Book.from_db_rows(row)
        return cls(
            book=book,
            quantity=row.get("quantity_available", 0),
            restock_threshold=row.get("restock_threshold", 2),
        )

    def custom_repr(self) -> str:
        return (
            f"Inventory(book={self.book}), "
            f"Quantity={self.quantity}, "
            f"restock_threshold={self.restock_threshold})"
        )

    """
    example use case of the above

        row = {
        "book_id": 1,
        "quantity": "2",
        "restock_threshold": False
    }

    inventory = Inventory.from_db_rows(row)
    print(inventory) 
"""
