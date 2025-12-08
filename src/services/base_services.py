from typing import Any
from abc import ABC, abstractmethod
from data.dataclasses.db_dataclass import DB
from data.database.dbconn import execute_query


class FilterBuilder(ABC):
    def __init__(self, db_session: DB) -> None:
        self._db = db_session

    @abstractmethod
    def build_conditions(self, filters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        pass


class DefaultFilterBuilder(FilterBuilder):
    def build_conditions(self, filters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        filters = {k: v for k, v in filters.items() if v is not None}
        if not filters:
            raise ValueError("At least one filter must be provided")
        conditions = " and ".join([f"{k} = :{k}" for k in filters.keys()])
        return conditions, filters


class QueryExecutor(ABC):
    def __init__(self, db_session: DB) -> None:
        self._db_session = db_session

    @property
    def db_session(self) -> DB:
        return self._db_session

    def execute(
        self, query: str, values: dict[str, Any] | None = None
    ) -> list[dict[str, Any]] | None:
        return execute_query(query, values, db_details=self.db_session)
