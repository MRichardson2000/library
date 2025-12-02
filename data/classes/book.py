from typing import Union, Any, Optional


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
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.deleted = deleted

    def __repr__(self) -> str:
        return f"Book: {self.title} by {self.author}\n Genre: {self.genre}\n Rating: {self.rating}."

    def filters(
        self, include_id: bool = False, include_deleted: bool = False
    ) -> dict[str, Any]:
        data: dict[str, Any] = {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "rating": self.rating,
        }
        if include_id:
            data["book_id"] = self.book_id
        if include_deleted:
            data["deleted"] = self.deleted
        return data

    def update_rating(self, new_rating: Union[int, float]) -> None:
        if not isinstance(new_rating, (int, float)):  # type: ignore
            raise TypeError(
                f"Rating must be int or float, not {type(new_rating).__name__}"
            )
        if 1 <= new_rating <= 5:
            self.rating = new_rating
        else:
            raise ValueError("The rating needs to be between 1 and 5.")
