from src.services.exceptions import DatabaseServiceError
from src.services.base_services import BaseService
from data.database.sql_models import users_insert
from data.dataclasses.db_dataclass import DB
from data.classes.user import User
from data.database.dbconn import execute_query
from typing import Any


class UserRepository:
    def __init__(self, db_details: DB) -> None:
        self.db_details = db_details

    def find_by_filters(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        conditions, params = BaseService.build_conditions(filters)
        query = f"select * from users where {conditions} and deleted = false"
        result = execute_query(query, params, self.db_details) or []
        return result

    def insert(self, user: User) -> None:
        try:
            execute_query(users_insert, user.filters(), self.db_details)
        except Exception as e:
            raise DatabaseServiceError("Failed to insert user") from e
