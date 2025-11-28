from __future__ import annotations
from data.classes.inventory import Inventory
from data.classes.book import Book
from data.database.dbconn import execute_query
from data.database.models import inventory_insert
from typing import Any


class InventoryServices:
    def __init__(self) -> None:
        pass

    # def add_stock(self, amount: int, book: Book) -> bool:
    #     """
    #     .

    #     Args:

    #     Returns:

    #     Raises:

    #     Notes:

    #     """
    #     try:
    #         filters: dict[str, Any]
