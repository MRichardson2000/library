from dotenv import load_dotenv
from data.dataclasses import DB
from data.models import book_table, cart_table, users_table, inventory_table
import os
import sqlalchemy as sa
from sqlalchemy.engine import Engine, Result
from typing import Optional, Any, List


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
            print(f"Create schema failed due to: {e}")


def execute_query(
    db_details: DB, query: str, params: tuple[Any, ...] = ()
) -> Optional[list[dict[str, Any]]]:
    engine: Engine = get_engine(db_details)
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            result: Result[Any] = conn.execute(sa.text(query), params)
            if query.strip().lower().startswith("select"):
                rows: List[dict[str, Any]] = [dict(row) for row in result.fetchall()]
                return rows
            trans.commit()
            return []
        except Exception as e:
            trans.rollback()
            print(f"Execute Query failed due to: {e}")
            return []


def create_schemas() -> None:
    db_details = load_env()
    create_schema(db_details, users_table)
    create_schema(db_details, book_table)
    create_schema(db_details, inventory_table)
    create_schema(db_details, cart_table)


def main() -> None:
    create_schemas()


if __name__ == "__main__":
    main()
