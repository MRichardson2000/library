from data.database.dbconn import fetch_result, execute_query
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from data.classes.inventory import Inventory


class InventoryQueries:
    def __init__(self, db_session: DB) -> None:
        self.db_session = db_session

    def get_inventory_availability(self, book: Book) -> bool:
        """
        Check if a book is available in inventory.

        Args:
            book: The book to check availability for.

        Returns:
            True if the book is available, False otherwise.
        """
        rows = fetch_result(
            """
            select i.is_available
            from b book
            left join inventory i on b.book_id = i.book_id
            where b.title = :title
            """,
            {"title": book.title},
            db_details=self.db_session,
        )
        if not rows:
            return False
        value = rows[0].get("is_available")
        return bool(value)

    def get_inventory_quantity(self, book: Book) -> int | None:
        """
        Get the available quantity of a book in inventory.

        Args:
            book: The book to get quantity for.

        Returns:
            The quantity available or None if not found.
        """
        rows = fetch_result(
            """
            select i.quantity_available
            from b book
            left join inventory i on b.book_id = i.book_id
            where b.title = :title
            """,
            {"title": book.title},
            db_details=self.db_session,
        )
        value = rows[0].get("quantity_available")
        return value

    def update_inventory_quantity(self, book: Book, inventory: Inventory) -> None:
        """
        Update the available quantity for a book in inventory.

        Args:
            book: The book to update.
            inventory: The inventory object containing the new quantity.
        """
        execute_query(
            """
            update inventory
            set quantity_available = :quantity_available
            where book_id = :book_id
            """,
            {
                "quantity_available": inventory.quantity,
                "book_id": book.book_id,
            },
            db_details=self.db_session,
        )
