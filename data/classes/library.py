from data.classes.book import Book
from data.classes.user import User
from data.classes.inventory import Inventory


class Library:
    def __init__(self) -> None:
        self.books: list[Book] = []
        self.users: list[User] = []
        self.inventory: list[Inventory] = []
