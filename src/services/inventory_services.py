from __future__ import annotations
from data.database.dbconn import execute_query, fetch_result
from data.classes.book import Book
from data.classes.inventory import Inventory
from src.services.exceptions import DatabaseServiceError
from typing import Any


class InventoryServices:
    def __init__(
        self,
        book: Book,
        inventory: Inventory,
        quantity_available: int,
        is_available: bool = False,
        restock_threshold: int = 2,
    ) -> None:
        self.book = book
        self.inventory = inventory
        self.quantity_available = quantity_available
        self.is_available = is_available
        self.restock_threshold = restock_threshold

    def get_quantity(self) -> int:
        try:
            book_id = fetch_result(
                "select book_id from book where title = :title",
                {"title": self.book.title},
            )[0]
            return fetch_result(
                "select quantity_available from inventory where book_id = :book_id",
                {"book_id": book_id},
            )[0]["quantity_available"]
        except Exception as e:
            raise DatabaseServiceError(
                "Failed to retrieve quantity in inventory"
            ) from e

    def get_availability(self) -> str:
        try:
            book_id = fetch_result(
                "select book_id from book where title = :title",
                {"title": self.book.title},
            )
            availability = fetch_result(
                "select is_available from inventory where book_id = :book_id",
                {"book_id": book_id},
            )[0]["is_available"]
            return availability
        except Exception as e:
            raise DatabaseServiceError("Unable to retrieve availability") from e

    def update_quantity(self) -> None:
        pass
