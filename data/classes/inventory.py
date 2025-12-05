from typing import Optional


class Inventory:
    def __init__(self, book_id: Optional[int], quantity: int) -> None:
        self._book_id = book_id
        self._quantity = quantity

    @property
    def book_id(self) -> Optional[int]:
        return self._book_id

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
        return self._quantity < 2
