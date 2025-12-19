from data.database.dbconn import execute_query, load_env
from data.dataclasses.db_dataclass import DB


def auto_clear_table(table: str, db: DB = load_env(testing=True)) -> None:
    execute_query(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")
