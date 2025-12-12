from typing import Any


class Book:
    def __init__(
        self,
        title: str,
        author: str,
        genre: str,
        rating: float,
        book_id: int | None = None,
        deleted: bool = False,
    ) -> None:
        self._book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.deleted = deleted

    def __repr__(self) -> str:
        return f"Book: {self.title} by {self.author} Genre: {self.genre} Rating: {self.rating}."

    @classmethod
    def from_db_row(cls, row: dict[str, Any]) -> "Book":
        return cls(
            book_id=row.get("book_id"),
            title=row.get("title", ""),
            author=row.get("author", ""),
            genre=row.get("genre", ""),
            rating=row.get("rating", 0.0),
            deleted=row.get("deleted", False),
        )
