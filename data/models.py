users_table = """
    create table if not exists users (
        unique_id bigserial primary key,
        user_id int not null unique,
        first_name text not null,
        last_name text not null,
        email_address text not null,
        phone_number bigint not null,
        books_loaned text not null
    );
"""

users_insert = """
    insert into users (
        user_id,
        first_name,
        last_name,
        email_address,
        phone_number,
        books_loaned
    ) values (
        :user_id,
        :first_name,
        :last_name,
        :email_address,
        :phone_number,
        :books_loaned
    );
"""

book_table = """
    create table if not exists book (
        unique_id bigserial primary key,
        book_id int not null unique,
        title text not null,
        author text not null,
        genre text not null,
        rating text not null
    );
"""

book_insert = """
    insert into book (
        book_id,
        title,
        author,
        genre,
        rating
    ) values (
        :book_id,
        :title,
        :author,
        :genre,
        :rating
    );
"""

inventory_table = """
    create table if not exists inventory (
        unique_id bigserial primary key,
        book_id int not null references book(book_id),
        quantity_available int not null,
        shelf_location text not null,
        is_available boolean not null default true
    );
"""

inventory_insert = """
    insert into inventory (
        book_id,
        quantity_available,
        shelf_location,
        is_available
    ) values (
        :book_id,
        :quantity_available,
        :shelf_location,
        :is_available
    );
"""

cart_table = """
    create table if not exists cart (
        unique_id bigserial primary key,
        user_id int not null references users(user_id),
        book_list text not null,
        borrow_date timestamp not null,
        return_date timestamp not null,
        late_return boolean not null default false,
        late_fee money
    );
"""

cart_insert = """
    insert into cart (
        user_id,
        book_list,
        borrow_date,
        return_date,
        late_return,
        late_fee
    ) values (
        :user_id,
        :book_list,
        :borrow_date,
        :return_date,
        :late_return,
        :late_fee
    );
"""
