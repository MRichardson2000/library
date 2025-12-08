from src.services.exceptions import DatabaseServiceError
from src.services.base_services import DefaultFilterBuilder, QueryExecutor
from data.database.sql_models import users_insert
from data.dataclasses.db_dataclass import DB
from data.classes.user import User
from typing import Any


class UserRepository:
    def __init__(self, db: DB) -> None:
        self.filters = DefaultFilterBuilder(db)
        self.executor = QueryExecutor(db)
        self.db = db

    def find_by_filters(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        conditions, params = self.filters.build_conditions(filters)
        query = f"select * from users where {conditions} and deleted = false"
        result = self.executor.execute(query, params) or []
        return result

    def insert(self, user: User) -> None:
        try:
            self.executor.execute(users_insert, user.filters())
        except Exception as e:
            raise DatabaseServiceError("Failed to insert user") from e
