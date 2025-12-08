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
    def __init__(self, db_session: DB, filter_builder: FilterBuilder) -> None:
        self._filter_builder = filter_builder
        self._db_session = db_session

    @property
    @abstractmethod
    def table_name(self) -> str:
        pass

    @property
    def db_session(self) -> DB:
        return self._db_session

    def execute(
        self, query: str, values: dict[str, Any] | None = None
    ) -> list[dict[str, Any]] | None:
        return execute_query(query, values, db_details=self.db_session)

    def find_by_filters(self, filters: dict[str, Any]) -> list[dict[str, Any]] | None:
        conditions, values = self._filter_builder.build_conditions(filters)
        query = f"select * from {self.table_name} where {conditions}"
        return self.execute(query, values)


class UserQueryExecutor(QueryExecutor):
    def __init__(self, db_session: DB) -> None:
        super().__init__(db_session, DefaultFilterBuilder(db_session))

    @property
    def table_name(self) -> str:
        return "users"


class BookQueryExecutor(QueryExecutor):
    def __init__(self, db_session: DB) -> None:
        super().__init__(db_session, DefaultFilterBuilder(db_session))

    @property
    def table_name(self) -> str:
        return "book"


class LoanQueryExecutor(QueryExecutor):
    def __init__(self, db_session: DB) -> None:
        super().__init__(db_session, DefaultFilterBuilder(db_session))

    @property
    def table_name(self) -> str:
        return "loan"
