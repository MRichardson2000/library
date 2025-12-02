from dotenv import load_dotenv
from data.dataclasses.db_dataclass import DB
from data.database.models import book_table, users_table, inventory_table, loan_table
from src.services.exceptions import DatabaseServiceError
import os
import sqlalchemy as sa
from sqlalchemy.engine import Engine
from typing import Optional, Any, Union, Sequence


def load_env(testing: bool = False) -> DB:
    dotenv_path = ".env.test" if testing else ".env"
    load_dotenv(dotenv_path=dotenv_path, override=True)
    print("Loaded DB Name:", os.getenv("DB_NAME"))
    if testing and os.getenv("DB_NAME") == "library":
        raise RuntimeError(
            "Test mode is using the prod DB - Check your .env.test file!"
        )
    db_details = DB(
        db_user=os.getenv("DB_USER", ""),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_host=os.getenv("DB_HOST", ""),
        db_port=os.getenv("DB_PORT", ""),
        db_name=os.getenv("DB_NAME", ""),
    )
    return db_details


def get_engine(db_details: DB) -> sa.Engine:
    url = (
        f"postgresql://{db_details.db_user}:{db_details.db_password}"
        f"@{db_details.db_host}:{db_details.db_port}/{db_details.db_name}"
    )
    return sa.create_engine(url)


def create_schema(
    db_details: DB, query: str, params: Optional[dict[str, Any]] = None
) -> None:
    engine = get_engine(db_details)
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(sa.text(query), params or {})
            trans.commit()
        except Exception as e:
            trans.rollback()
            raise DatabaseServiceError("Create schema failed") from e


def execute_query(
    query: str,
    params: Optional[Union[Sequence[Any], dict[str, Any]]] = None,
    db_details: Optional[DB] = None,
) -> Optional[list[dict[str, Any]]]:
    if db_details is None:
        db_details = load_env()
    engine: Engine = get_engine(db_details)
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            result = conn.execute(sa.text(query), params or {})
            if query.strip().lower().startswith("select"):
                rows = result.mappings().all()
                return [dict(r) for r in rows]
            trans.commit()
        except Exception as e:
            trans.rollback()
            raise DatabaseServiceError("Execute query failed") from e


def create_schemas() -> None:
    db_details = load_env(testing=True)
    create_schema(db_details, users_table)
    create_schema(db_details, book_table)
    create_schema(db_details, loan_table)
    create_schema(db_details, inventory_table)


def main() -> None:
    create_schemas()


if __name__ == "__main__":
    main()
