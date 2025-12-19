from data.csv_handler import CsvIngestion
from data.database.dbconn import load_env
from src.services.loan_services import LoanServices, LoanQueries
from src.services.book_services import BookQueries
from src.services.user_services import UserQueries
from data.classes.user import User
from data.classes.book import Book
from data.classes.inventory import Inventory
from data.classes.loan import Loan
from data.dataclasses.db_dataclass import DB
from datetime import datetime


def ingest_data(db_session: DB) -> None:
    data_ingestion = CsvIngestion(db_session)
    data_ingestion.load_cust()
    data_ingestion.load_book()


def checkout_book(db_session: DB, user: User, book: Book) -> None:
    loan_queries = LoanQueries(db_session)
    inventory = Inventory(book, 1)
    loan = Loan(book, user, inventory)
    loan.borrow_book()

    LoanServices(
        user=user,
        loan=loan,
        loan_queries=loan_queries,
        inventory=inventory,
        book=book,
    )
    loan_queries.insert_loan(loan.book)


def main() -> None:
    db_session = load_env(testing=False)
    today = datetime.today()
    if today.day == 1:
        ingest_data(db_session)
    user_queries = UserQueries(db_session)
    book_queries = BookQueries(db_session)

    user = user_queries.find_user("MarcusRichardson2000@gmail.com")
    book = Book("Fourth Wing", "Rebecca Yarris(I think)", "Fantasy", 5.0)
    book_rows = book_queries.find_by_title(book)

    if user and book_rows:
        row = book_rows[0]
        book_obj = Book(row["title"], row["author"], row["genre"], float(row["rating"]))
        checkout_book(db_session, user, book_obj)


if __name__ == "__main__":
    main()
