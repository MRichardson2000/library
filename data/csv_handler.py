from __future__ import annotations
from data.config import FILES_FOLDER
from pathlib import Path
from data.dataclasses.db_dataclass import DB
from data.classes.user import User
from data.classes.book import Book
from src.services.user_services import UserQueries, UserServices
from src.services.book_services import BookQueries, BookServices
import csv


class CsvIngestion:
    def __init__(self, db_session: DB) -> None:
        self.db_session = db_session

    def load_cust(self, folder: Path = FILES_FOLDER, testing: bool = False) -> None:
        cust_file = folder / "cust.csv" if not testing else folder / "test_cust.csv"
        with open(cust_file, "r", newline="") as f:
            reader = csv.DictReader(f)
            user_rows = [row for row in reader]
            for row in user_rows:
                user = User.from_csv_row(row)
                queries = UserQueries(self.db_session)
                service = UserServices(user, queries)
                service.create_user()

    def load_book(self, folder: Path = FILES_FOLDER, testing: bool = False) -> None:
        book_file = folder / "book.csv" if not testing else folder / "test_book.csv"
        with open(book_file, "r", newline="") as f:
            reader = csv.DictReader(f)
            book_rows = [row for row in reader]
            for row in book_rows:
                book = Book.from_csv_row(row)
                queries = BookQueries(self.db_session)
                service = BookServices(book, queries)
                service.create_book()
