from __future__ import annotations
from data.database.queries.inventory_queries import InventoryQueries
from data.classes.book import Book
from data.classes.inventory import Inventory
from src.services.exceptions import DatabaseServiceError


class InventoryServices:
    def __init__(
        self,
        book: Book,
        inventory: Inventory,
        inventory_queries: InventoryQueries,
        quantity_available: int,
        is_available: bool = False,
        restock_threshold: int = 2,
    ) -> None:
        self.book = book
        self.inventory = inventory
        self.inventory_queries = inventory_queries
        self.quantity_available = quantity_available
        self.is_available = is_available
        self.restock_threshold = restock_threshold

    def get_quantity(self) -> int | None:
        try:
            return self.inventory_queries.get_inventory_quantity(self.book)
        except Exception as e:
            raise DatabaseServiceError(
                "Failed to retrieve quantity in inventory"
            ) from e

    def get_availability(self) -> bool:
        try:
            return self.inventory_queries.get_inventory_availability(self.book)
        except Exception as e:
            raise DatabaseServiceError("Unable to retrieve availability") from e

    def update_quantity(self) -> None:
        self.inventory.add_stock()
        try:
            self.inventory_queries.update_inventory_quantity(self.book, self.inventory)
        except Exception as e:
            raise DatabaseServiceError("Failed to update quantity") from e
