from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email_address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_number: Mapped[int] = mapped_column(Integer, nullable=False)


class BookORM(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    genre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    rating: Mapped[int | float] = mapped_column(Integer, Float, nullable=False)
