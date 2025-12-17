from typing import Any
from data.classes.enums import BookState


class Book:
    def __init__(
        self,
        title: str,
        author: str,
        genre: str,
        rating: float,
        book_id: int | None = None,
        status: BookState = BookState.AVAILABLE,
    ) -> None:
        self._book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.status = status

    def __repr__(self) -> str:
        return f"Book: {self.title} by {self.author} Genre: {self.genre} Rating: {self.rating}."

    @property
    def book_id(self) -> int | None:
        return self._book_id

    @classmethod
    def from_db_row(cls, row: dict[str, Any]) -> "Book":
        return cls(
            book_id=row.get("book_id"),
            title=row.get("title", ""),
            author=row.get("author", ""),
            genre=row.get("genre", ""),
            rating=row.get("rating", 0.0),
            status=row.get("status", False),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "book_id": self._book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "rating": self.rating,
            "status": self.status,
        }
