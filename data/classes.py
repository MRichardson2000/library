from datetime import datetime


class Book:
    def __init__(
        self, book_id: int, title: str, author: str, genre: str, rating: int | float
    ) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating

    def __repr__(self) -> str:
        return f"Book({self.title} by {self.author})"


class User:
    def __init__(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: int,
        books_loaned: list[Book],
    ) -> None:
        self.user = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.books_loaned = books_loaned


class Inventory:
    def __init__(
        self,
        book_id: int,
        quantity_available: int,
        shelf_location: str,
        is_available: bool,
    ) -> None:
        self.book_id = book_id
        self.quantity_available = quantity_available
        self.shelf_location = shelf_location
        self.is_available = is_available


class Cart:
    def __init__(
        self,
        user: User,
        book_list: list[Book],
        borrow_date: datetime,
        return_date: datetime,
        late_return: bool,
        late_fee: int,
    ) -> None:
        self.user = user
        self.book_list = book_list
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.late_return = late_return
        self.late_fee = late_fee
