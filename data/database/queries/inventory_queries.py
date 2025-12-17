from data.database.queries.base_queries import Queries
from data.database.dbconn import fetch_result, execute_query


class InventoryQueries(Queries):
    def get_inventory_availability(self) -> bool:
        rows = fetch_result(
            """
            select i.is_available
            from b book
            left join inventory i on b.book_id = i.book_id
            where b.title = :title
            """,
            {"title": self.book.title},
        )
        if not rows:
            return False
        value = rows[0].get("is_available")
        return bool(value)

    def get_inventory_quantity(self) -> int | None:
        rows = fetch_result(
            """
            select i.quantity_available
            from b book
            left join inventory i on b.book_id = i.book_id
            where b.title = :title
            """,
            {"title": self.book.title},
        )
        value = rows[0].get("quantity_available")
        return value

    def update_inventory_quantity(self) -> None:
        execute_query(
            """
            update i.inventory
            left join b book
            on i.book_id = b.book_id
            set quantity_available = :quantity_available
            where book_id = :book_id
            """,
            {
                "quantity_available": self.inventory.quantity,
                "book_id": self.book.book_id,
            },
        )
