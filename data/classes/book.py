from typing import Union, Optional, Any


class Book:
    def __init__(
        self,
        book_id: Optional[int],
        title: str,
        author: str,
        genre: str,
        rating: Union[int, float],
        deleted: bool = False,
    ) -> None:
        self._book_id = book_id
        self._title = title
        self._author = author
        self._genre = genre
        Book.validate_rating(rating)
        self._rating = rating
        self.deleted = deleted

    def __repr__(self) -> str:
        return f"Book: {self.title} by {self.author}\n Genre: {self.genre}\n Rating: {self.rating}."

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        if self.book_id is not None and other.book_id is not None:
            return self.book_id == other.book_id
        return (self.title, self.author) == (other.title, other.author)

    def __hash__(self) -> int:
        if self.book_id is not None:
            return hash(self.book_id)
        return hash((self.title, self.author))

    @property
    def book_id(self) -> Optional[int]:
        return self._book_id

    @book_id.setter
    def book_id(self, value: int) -> None:
        self._book_id = value

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def genre(self) -> str:
        return self._genre

    @genre.setter
    def genre(self, new_genre: str) -> None:
        self._genre = new_genre

    @property
    def rating(self) -> Union[int, float]:
        return self._rating

    @rating.setter
    def rating(self, new_rating: Union[int, float]) -> None:
        Book.validate_rating(new_rating)
        self._rating = new_rating

    def mark_deleted(self) -> None:
        self.deleted = True

    def restore(self) -> None:
        self.deleted = False

    def filters(self) -> dict[str, Any]:
        return {
            "title": self._title,
            "author": self._author,
            "genre": self._genre,
            "rating": self.rating,
        }

    def id_filter(self) -> dict[str, Any]:
        return {"book_id": self.book_id}

    @classmethod
    def from_db_rows(cls, row: dict[str, Any]) -> "Book":
        return cls(
            book_id=row.get("book_id"),
            title=row.get("title", ""),
            author=row.get("author", ""),
            genre=row.get("genre", ""),
            rating=row.get("rating", 1),
            deleted=row.get("deleted", False),
        )

    """
    example use case of the above

        row = {
        "book_id": 1,
        "title": "1984",
        "author": "George Orwell",
        "genre": "Dystopian",
        "rating": 5,
        "deleted": False,
    }

    book = Book.from_db_row(row)
    print(book) 
"""

    @staticmethod
    def validate_rating(rating: Union[int, float]) -> None:
        if not isinstance(rating, (int, float)):  # type: ignore
            raise TypeError("Rating must be int or float")
        if not (1 <= rating <= 5):
            raise ValueError("The rating must be between 1 and 5")
