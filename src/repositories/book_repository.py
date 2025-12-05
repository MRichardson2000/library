from sqlalchemy.orm import Session
from data.database.orm_models import BookORM
from src.services.exceptions import DatabaseServiceError, UserAlreadyExistsError
from typing import Any


class BookRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_title(self, book_title: str) -> BookORM | None:
        return (
            self.session.query(BookORM)
            .filter(BookORM.book_title == book_title)
            .one_or_none()
        )
