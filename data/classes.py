from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional


class Library:
    def __init__(self) -> None:
        self.books: list[Book] = []
        self.book_status: list[BookStatus] = []
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
    ) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.status = BookStatus()

    def __repr__(self) -> str:
        return f"Book: {self.title} by {self.author}\n Genre: {self.genre}\n Rating: {self.rating}\n Book Status{self.status}"

    def update_rating(self, new_rating: int | float) -> str:
        if not isinstance(new_rating, (int, float)):  # type: ignore
            raise TypeError(
                f"Rating must be int or float - strings are not allowed, You entered: {type(new_rating)}"
            )
        if new_rating > 0 and new_rating <= 5:
            old_rating = self.rating
            self.rating = new_rating
            return f"The rating of {self.title} has been updated from {old_rating} to {new_rating}"
        else:
            return f"The rating of {self.title} can't be less than 0 or greater than 5"


class BookStatus:
    def __init__(
        self,
        checked_in: bool = True,
        checked_out: bool = False,
        stolen: bool = False,
        damaged: bool = False,
        sold: bool = False,
        refurbished: bool = False,
        new: bool = True,
        responsible_party: User | None = None,
    ) -> None:
        self.checked_in = checked_in
        self.checked_out = checked_out
        self.stolen = stolen
        self.damaged = damaged
        self.sold = sold
        self.refurbished = refurbished
        self.new = new
        self.responsible_party = responsible_party
        self.book_loan_timings = BookLoanTimings()

    def __repr__(self) -> str:
        flags: list[str] = []
        if self.stolen:
            flags.append("stolen")
        if self.damaged:
            flags.append("damaged")
        if self.sold:
            flags.append("sold")
        if self.refurbished:
            flags.append("refurbished")
        if self.new:
            flags.append("new")
        if self.checked_out and self.responsible_party:
            flags.append(f"On loan by: {self.responsible_party}")
        return f"BookStatus: {', '.join(flags) or 'none'}"

    def damaged_book(self, book: "Book") -> str:
        self.damaged = True
        return f"{book.title} has been damaged. {self.responsible_party}: to pay a replacement fee of £5. Please make this payment within the next 7 days at the reception desk."

    def sold_book(self, book: "Book") -> str:
        self.sold = True
        return f"{book.title} has been sold to {self.responsible_party}. Thank you!"

    def stolen_book(self, book: "Book", timing: BookLoanTimings) -> str:
        """TODO - Finish this off"""
        self.stolen = True
        if self.checked_out:
            return "ignore for now coming back to it"
        else:
            return "ignore for now coming back to it"

    def checkout_book(self, book: Book, user: "User") -> str:
        if not self.checked_out:
            self.checked_out = True
            self.responsible_party = user
            time_borrowed = self.book_loan_timings.borrow_time()
            return f"{book.title} has been checked out to {user.first_name} {user.last_name} \n {time_borrowed}"
        else:
            return f"{book.title} is already checked out."

    def checkin_book(self, book: "Book") -> str:
        if self.checked_out:
            self.checked_out = False
            self.checked_in = True
            return f"{book.title} has been checked in by {self.responsible_party}. The Library hopes you enjoyed this book!"
        else:
            return f"{book.title} is already checked in."


class BookLoanTimings:
    def __init__(self) -> None:
        self.borrowed_datetime = datetime.now()

    def borrow_time(self) -> str:
        self.borrowed_datetime = datetime.now()
        cleaned_borrowed_datetime = self.borrowed_datetime.strftime("%Y-%m-%d %H:%M")
        return_datetime = self.borrowed_datetime + timedelta(days=30)
        cleaned_return_datetime = return_datetime.strftime("%Y-%m-%d %H:%M")
        return f"Book borrowed on: {cleaned_borrowed_datetime}. \n Please return on: {cleaned_return_datetime} to avoid a late fee charge."

    def late_return(self, book: Book) -> str:
        now = datetime.now()
        late_threshold = self.borrowed_datetime + timedelta(days=30)
        if now > late_threshold:
            return (
                f"{book.title}: has been returned late. There is a late fee of £2.50."
            )
        else:
            return f"{book.title}: has been returned on time. There is no late fee."

    def extend_borrow_time(self, book: Book) -> str:
        self.borrowed_datetime = datetime.now()
        new_return_date = self.borrowed_datetime + timedelta(days=30)
        cleaned_datetime = new_return_date.strftime("%Y-%m-%d %H:%M")
        return f"{book.title} has been extended for another 30 days. Please return on {cleaned_datetime}"


class User:
    def __init__(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: int,
        books_loaned: Optional[list[Book]] = None,
    ) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.books_loaned = books_loaned if books_loaned is not None else []

    def __repr__(self) -> str:
        return f"User: {self.first_name} {self.last_name}, {len(self.books_loaned)} books loaned."

    def surname_change(self, new_last_name: str) -> str:
        self.last_name = new_last_name
        return f"Surname has been updated to {new_last_name} as requested."

    def new_email(self, new_email: str) -> str:
        self.email_address = new_email
        return f"Email address has been updated to {new_email} as requested."

    def new_phone_number(self, new_phone_num: int) -> str:
        self.phone_number = new_phone_num
        return f"Phone number has been updated to {new_phone_num} as requested."

    def books_on_loan(self) -> str:
        book_length = len(self.books_loaned)
        return f"{self.first_name} has: {book_length} books loaned."


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

    def update_quantity(self, available_items: int) -> None:
        self.quantity_available = available_items

    def update_availability(self) -> None:
        self.is_available = True


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


if __name__ == "__main__":
    book = Book(1, "test", "test", "test", 4)
    print(book.update_rating(3))
    print(book)
