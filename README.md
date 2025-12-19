**Library Management — Python Project**

**Project Overview**:
- **Purpose:** A small, well-structured Python library management application that demonstrates CSV data ingestion, a simple database layer, domain classes (books, users, inventory, loans), and service-layer logic with unit tests.
- **Audience:** Designed to showcase backend design, testing, and clean code practices.

**Highlights**:
- **Modular design:** separation of data access (`data/`), domain classes (`data/classes/`), service logic (`src/services/`), and tests (`tests/`).
- **Data ingestion:** CSV import tooling lives in `data/csv_handler.py` and is exercised by `main.py` when enabled.
- **Test coverage:** Unit tests are organized under `tests/` to validate key flows (users, books, loans, inventory).

**Tech Stack**:
- **Language:** Python 3 (see `pyproject.toml`)
- **Storage:** Local SQL database connection code under `data/database/` (configurable via `data/database/dbconn.py`). - postgres dbms
- **Testing:** pytest (tests located in `tests/`).

**Key Features**:
- CSV ingestion for customers and books (`data/csv_handler.py`).
- CRUD-like queries and query helpers in `data/database/queries/`.
- Service layer for business logic in `src/services/` (loan, book, user, inventory logic).
- Example runner in `main.py` to demonstrate common flows like ingesting data and checking out a book.

**Project Structure (important files)**
- **Entry point:** [main.py](main.py) — example runner for ingesting data and creating a loan.
- **CSV ingestion:** [data/csv_handler.py](data/csv_handler.py)
- **Database connection & models:** [data/database/dbconn.py](data/database/dbconn.py) and [data/database/sql_models.py](data/database/sql_models.py)
- **Service layer:** [src/services/book_services.py](src/services/book_services.py), [src/services/loan_services.py](src/services/loan_services.py), [src/services/user_services.py](src/services/user_services.py)
- **Tests:** [tests](tests) — unit tests that exercise the core behavior and business rules.

**Getting started**
1. Create a virtual environment and activate it. 

```bash
uv venv - install uv with pip install uv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies. use the `pyproject.toml` and run uv sync in the terminal:

3. Run the example script:

```bash
uv run main.py
```

4. Run tests:

```bash
pytest -q
```

- This repository focuses on clean separation of concerns: data ingestion, persistence layer, domain classes, and service/business logic — all covered by unit tests to illustrate design and reliability.

---

Author
Marcus Richardson

