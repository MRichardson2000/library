from data.database.queries.base_queries import Queries
from data.database.sql_models import loan_insert
from data.database.dbconn import fetch_result, execute_query
from datetime import datetime
from typing import Any


class LoanQueries(Queries):
    def insert_loan(self) -> None:
        execute_query(loan_insert, self.book.to_dict())

    def end_loan(self) -> None:
        execute_query(
            """
            update loan
            set status = returned
            where book_id = :book_id
            """,
            {"book_id": self.book.book_id},
        )

    def get_books_on_loan(self) -> list[dict[str, Any]] | None:
        rows = execute_query(
            """
            select b.title
                   from loan l
                   left join book b on l.book_id = b.book_id
                   left join users u on l.user_id = u.user_id
                   where l.status = 'Borrowed'
                   and u.first_name = :first_name
                   and u.last_name = :last_name
            """,
            {"first_name": self.user.first_name, "last_name": self.user.last_name},
        )
        if rows:
            return rows

    def loan_extension(self) -> None:
        execute_query(
            "update loan set due_date = :due_date", {"due_date": self.loan.due_date}
        )

    def due_date_retrieval(self) -> datetime | None:
        rows = fetch_result(
            "select due_date from loan where book_id = :book_id and status = 'Borrowed'",
            {"title": self.book.title},
        )
        if rows:
            values = rows[0].get("due_date")
            return values

    def verification(self) -> None:
        self.max_book_number_check()

    def max_book_number_check(self) -> bool:
        rows = fetch_result(
            """
            select b.title
                from loan l
                left join book b on l.book_id = b.book_id
                left join users u on l.user_id = u.user_id
                where l.status = 'Borrowed'
                and u.first_name = :first_name
                and u.last_name = :last_name
            """,
            {"first_name": self.user.first_name, "last_name": self.user.last_name},
        )
        books = [book for book in rows]
        return False if len(books) == 5 else True
