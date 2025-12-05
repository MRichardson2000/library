from sqlalchemy.orm import Session
from data.database.orm_models import UserORM
from src.services.exceptions import DatabaseServiceError, UserAlreadyExistsError
from typing import Any


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_email(self, email_address: str) -> UserORM | None:
        return (
            self.session.query(UserORM)
            .filter(UserORM.email_address == email_address)
            .one_or_none()
        )

    def find_by_filters(self, filters: dict[str, Any]) -> list[UserORM]:
        filters = {k: v for k, v in filters.items() if v is not None}
        query = self.session.query(UserORM)
        for field, value in filters.items():
            if hasattr(UserORM, field):
                query = query.filter(getattr(UserORM, field) == value)
        return query.all()

    def insert(self, user: UserORM) -> None:
        try:
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise DatabaseServiceError("Failed to insert user") from e

    def assert_not_exists_by_email(self, email_address: str) -> None:
        if self.find_by_email(email_address):
            raise UserAlreadyExistsError("User already exists")
