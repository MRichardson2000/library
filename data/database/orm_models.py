from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email_address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_number: Mapped[int] = mapped_column(Integer, nullable=False)
