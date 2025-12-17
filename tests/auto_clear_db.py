from data.database.dbconn import execute_query, load_env
from data.dataclasses.db_dataclass import DB


def auto_clear_book_table(db: DB = load_env(testing=True)) -> None:
    execute_query("TRUNCATE book RESTART IDENTITY CASCADE;")


def auto_clear_user_table(db: DB = load_env(testing=True)) -> None:
    execute_query("TRUNCATE users RESTART IDENTITY CASCADE;")
