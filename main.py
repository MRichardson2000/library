from data.csv_handler import CsvIngestion
from data.database.dbconn import load_env


def main() -> None:
    data_ingestion = CsvIngestion(load_env())
    data_ingestion.load_cust()
    data_ingestion.load_book()


if __name__ == "__main__":
    main()
