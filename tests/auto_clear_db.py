from data.database.dbconn import execute_query, load_env
from data.dataclasses.db_dataclass import DB


def auto_clear_db(db: DB = load_env(testing=True)) -> None:
    execute_query("truncate book restart identity cascade", db_details=db)
    execute_query("ALTER SEQUENCE book_unique_id_seq RESTART WITH 1;", db_details=db)
