from data.database.dbconn import fetch_result, execute_query, load_env
from data.dataclasses.db_dataclass import DB
from data.classes.book import Book
from data.classes.inventory import Inventory


class InventoryQueries:
    def __init__(self, db_session: DB = load_env()) -> None:
        self.db_session = db_session

    def get_inventory_availability(self, book: Book) -> bool:
        rows = fetch_result(
            """
            select i.is_available
            from b book
            left join inventory i on b.book_id = i.book_id
            where b.title = :title
            """,
            {"title": book.title},
        )
        value = rows[0].get("is_available")
        return False if value else True
    
    def get_inventory_quantity(self, book: Book) -> int:
        rows = fetch_result(
            """
            select i.quantity_available
            from b book
            left join inventory i on b.book_id = i.book_id
            where b.title = :title
            """,
            {"title": book.title}
        )
        value = rows[0].get("quantity_available")
        return value if value else 0
        

    def update_inventory_quantity(self, book: Book, inventory: Inventory) -> None:
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
        )
