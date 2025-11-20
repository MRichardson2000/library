from datetime import datetime


class Library:
    def __init__(self) -> None:
        self.books: list[Book] = []
        self.users: list[User] = []
        self.inventory: list[Inventory] = []
        self.cart: list[Cart] = []


class Book:
    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        genre: str,
        rating: int | float,
        checkin_status: bool = False,
    ) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.checkin_status = checkin_status

    def __repr__(self) -> str:
        return f"Book({self.title} by {self.author})"

    def update_rating(self, new_rating: int | float) -> None:
        self.rating = new_rating

    def update_checkin_status(self) -> None:
        self.checkin_status = True


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
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.books_loaned = books_loaned

    def __repr__(self) -> str:
        return f"User: {self.first_name} {self.last_name}, {self.books_loaned} books loaned."

    def surname_change(self, new_last_name: str) -> None:
        self.last_name = new_last_name

    def new_email(self, new_email: str) -> None:
        self.email_address = new_email

    def new_phone_number(self, new_phone_num: int) -> None:
        self.phone_number = new_phone_num

    def update_books_loaned(self, book_name: str) -> str:
        for book in self.books_loaned:
            if book.title == book_name:
                book.update_checkin_status()
                return f"{book_name}: Checked in successfully"
        return f"{book_name}: not found in loaned books, unable to check in."


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
