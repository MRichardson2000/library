from dotenv import load_dotenv
from data.dataclasses.db_dataclass import DB
from data.database.sql_models import (
    book_table,
    users_table,
    inventory_table,
    loan_table,
)
from src.services.exceptions import DatabaseServiceError
import os
import sqlalchemy as sa
import logging
from typing import Any


def load_env(testing: bool = False) -> DB:
    dotenv_path = ".env.test" if testing else ".env"
    load_dotenv(dotenv_path=dotenv_path, override=True)
    logging.info("Loaded DB Name: %s", os.getenv("DB_NAME"))
    if testing and os.getenv("DB_NAME") == "library":
        raise RuntimeError(
            "Test mode is using the prod DB - Check your .env.test file!"
        )
    return DB(
        db_user=os.getenv("DB_USER", ""),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_host=os.getenv("DB_HOST", ""),
        db_port=os.getenv("DB_PORT", ""),
        db_name=os.getenv("DB_NAME", ""),
    )


def get_engine(db_details: DB = load_env()) -> sa.Engine:
    url = (
        f"postgresql://{db_details.db_user}:{db_details.db_password}"
        f"@{db_details.db_host}:{db_details.db_port}/{db_details.db_name}"
    )
    return sa.create_engine(url, echo=False, future=True)


def fetch_result(
    query: str, params: dict[str, Any] | None = None, db_details: DB | None = None
) -> list[dict[str, Any]]:
    engine = get_engine()
    try:
        with engine.begin() as conn:
            result = conn.execute(sa.text(query), params or {})
            return [dict(r) for r in result.mappings()]
    except Exception as e:
        raise DatabaseServiceError("Fetch results failed") from e


def execute_query(
    query: str, params: dict[str, Any] | None = None, db_details: DB | None = None
) -> None:
    engine = get_engine()
    try:
        with engine.begin() as conn:
            conn.execute(sa.text(query), params or {})
    except Exception as e:
        raise DatabaseServiceError("Execute query failed") from e


def create_schemas() -> None:
    print(" # --- Creating Users Table --- #")
    execute_query(users_table)
    print(" # --- Creating Book Table --- #")
    execute_query(book_table)
    print(" # --- Creating Inventory Table --- #")
    execute_query(inventory_table)
    print(" # --- Creating Loan Table --- #")
    execute_query(loan_table)


def main() -> None:
    create_schemas()


if __name__ == "__main__":
    main()
