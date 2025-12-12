from data.classes.book import Book
from typing import Any


class Inventory:
    def __init__(
        self,
        book: Book,
        quantity: int,
        inventory_id: int | None = None,
        restock_threshold: int = 2,
    ) -> None:
        self._inventory_id = inventory_id
        self.book = book
        self.quantity = quantity
        self.restock_threshold = restock_threshold

    def __repr__(self) -> str:
        return f"Inventory (book={self.book.title}, quantity={self.quantity}, current restock_threshold={self.restock_threshold})"

    @property
    def inventory_id(self) -> int | None:
        return self._inventory_id

    def add_stock(self, amount: int = 1) -> None:
        self.quantity += amount

    def remove_stock(self, amount: int = 1) -> None:
        if amount > self.quantity:
            raise ValueError("Not enough stock to remove")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self.quantity -= amount

    def availability(self) -> bool:
        return self.quantity > 0

    def needs_restock(self) -> bool:
        return self.quantity < self.restock_threshold

    @classmethod
    def from_db_row(cls, row: dict[str, Any], book: Book) -> "Inventory":
        book = Book.from_db_row(row)
        return cls(
            book=book,
            quantity=row.get("quantity_available", 0),
            restock_threshold=row.get("restock_threshold", 2),
            inventory_id=row.get("inventory_id"),
        )
