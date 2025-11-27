class Inventory:
    def __init__(
        self,
        book_id: int,
        book_quantity: int,
        shelf_location: str,
        availability: bool,
    ) -> None:
        self.book_id = book_id
        self.book_quantity = book_quantity
        self.shelf_location = shelf_location
        self.availability = availability

    def add_stock(self, quantity: int) -> None:
        self.book_quantity += quantity

    def remove_stock(self, quantity: int) -> None:
        if not quantity <= self.book_quantity:
            self.book_quantity -= quantity

    def get_quantity(self) -> int:
        return self.book_quantity

    def get_availability(self) -> bool:
        return self.book_quantity > 0

    def update_availability(self) -> None:
        self.availability = self.book_quantity > 0

    def needs_restock(self) -> bool:
        return self.book_quantity < 2
