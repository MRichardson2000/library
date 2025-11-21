from __future__ import annotations
from data.dbconn import execute_query
from data.dataclasses import DB
from data.classes import Book
from tests.conftests import db_session


def test_add_book(db: DB) -> None:
    book = Book(1, "test", "test", "test", 3)
