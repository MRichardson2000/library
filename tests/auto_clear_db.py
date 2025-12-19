from data.database.dbconn import execute_query
from data.dataclasses.db_dataclass import DB


def auto_clear_table(table: str, db_session: DB) -> None:
    execute_query(f"TRUNCATE {table} RESTART IDENTITY CASCADE;", db_details=db_session)
