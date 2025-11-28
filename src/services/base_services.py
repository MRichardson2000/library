from typing import Any


class BaseService:
    def __init__(self) -> None:
        pass

    def build_conditions(self, filters: dict[str, Any]) -> tuple[str, list[Any]]:
        filters = {k: v for k, v in filters.items() if v is not None}
        if not filters:
            raise ValueError("At least one filter must be provided")
        conditions = " and ".join([f"{k} = %s" for k in filters.keys()])
        values = list(filters.values())
        return conditions, values
