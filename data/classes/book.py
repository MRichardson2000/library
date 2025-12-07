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
        if not isinstance(rating, (int, float)):  # type: ignore
            raise TypeError(f"Rating must be int or float, not {type(rating).__name__}")
        if not (1 <= rating <= 5):
            raise ValueError("The rating needs to be between 1 and 5.")
        self._book_id = book_id
        self._title = title
        self._author = author
        self._genre = genre
        self._rating = rating
        self.deleted = deleted

    def __repr__(self) -> str:
        return f"Book: {self.title} by {self.author}\n Genre: {self.genre}\n Rating: {self.rating}."

    @property
    def book_id(self) -> Optional[int]:
        return self._book_id

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
        if not isinstance(new_rating, (int, float)):  # type: ignore
            raise TypeError(
                f"Rating must be int or float, not {type(new_rating).__name__}"
            )
        if not (1 <= new_rating <= 5):
            raise ValueError("The rating needs to be between 1 and 5.")
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
