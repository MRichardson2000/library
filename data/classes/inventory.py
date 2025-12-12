from data.classes.book import Book
from typing import Any, Optional


class Inventory:
    def __init__(
        self,
        book: Book,
        quantity: int,
        inventory_id: Optional[int],
        restock_threshold: int = 2,
    ) -> None:
        self.inventory_id = inventory_id
        self.book = book
        self._quantity = quantity
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
        self._quantity = new_quantity

    def add_stock(self, amount: int = 1) -> None:
        self._quantity += amount

    def remove_stock(self, amount: int = 1) -> None:
        if amount > self._quantity:
            raise ValueError("Not enough stock to remove")
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
            inventory_id=row.get("inventory_id"),
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
