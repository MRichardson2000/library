book_table = """
    create table if not exists book (
        unique_id bigserial primary key,
        title text not null,
        author text not null,
        genre text not null,
        price money not null,
        rating text not null
    );
"""

book_insert = """
INSERT INTO book (
    title,
    author,
    genre,
    price,
    rating
) VALUES (
    :title,
    :author,
    :genre,
    :price,
    :rating
);
"""
