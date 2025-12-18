from __future__ import annotations
from data.database.queries.inventory_queries import InventoryQueries
from data.classes.book import Book
from data.classes.inventory import Inventory
from src.services.exceptions import DatabaseServiceError
import logging


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
        logging.info("Attempting to get quantity of %s", self.book.title)
        try:
            logging.info("Retrieved quantity for %s successfully", self.book.title)
            return self.inventory_queries.get_inventory_quantity(self.book)
        except Exception as e:
            logging.exception("Failed to get quantity for %s", self.book.title)
            raise DatabaseServiceError(
                "Failed to retrieve quantity in inventory"
            ) from e

    def get_availability(self) -> bool:
        logging.info("Attempting to get availability of %s", self.book.title)
        try:
            logging.info("Successfully retrieved availability for %s", self.book.title)
            return self.inventory_queries.get_inventory_availability(self.book)
        except Exception as e:
            logging.exception("Failed to retrieve availability")
            raise DatabaseServiceError("Unable to retrieve availability") from e

    def update_quantity(self) -> None:
        logging.info("Attempting to update quantity of %s", self.book.title)
        self.inventory.add_stock()
        try:
            logging.info(
                "Successfully updated quantity of %s in the inventory database",
                self.book.title,
            )
            self.inventory_queries.update_inventory_quantity(self.book, self.inventory)
        except Exception as e:
            logging.exception("Failed to update quantity for %s", self.book.title)
            raise DatabaseServiceError("Failed to update quantity") from e
