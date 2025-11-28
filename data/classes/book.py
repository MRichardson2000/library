from typing import Union, Any


class Book:
    def __init__(
        self,
        book_id: int,
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

    def filters(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "rating": self.rating,
        }

    def update_rating(self, new_rating: Union[int, float]) -> None:
        if not isinstance(new_rating, (int, float)):  # type: ignore
            raise TypeError(
                f"Rating must be int or float, not {type(new_rating).__name__}"
            )
        if 1 <= new_rating <= 5:
            self.rating = new_rating
        else:
            raise ValueError("The rating needs to be between 1 and 5.")
