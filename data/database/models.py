users_table = """
    create table if not exists users (
        unique_id bigserial primary key,
        user_id int not null unique,
        first_name text not null,
        last_name text not null,
        email_address text not null,
        phone_number bigint not null,
        books_loaned text not null,
        deleted bool not null default false
    );
"""

users_insert = """
    insert into users (
        user_id,
        first_name,
        last_name,
        email_address,
        phone_number,
        books_loaned,
        deleted
    ) values (
        :user_id,
        :first_name,
        :last_name,
        :email_address,
        :phone_number,
        :books_loaned,
        :deleted
    );
"""

book_table = """
    create table if not exists book (
        unique_id bigserial primary key,
        book_id int not null unique,
        title text not null,
        author text not null,
        genre text not null,
        rating text not null,
        deleted bool not null default false
    );
"""

book_insert = """
    insert into book (
        book_id,
        title,
        author,
        genre,
        rating,
        deleted
    ) values (
        :book_id,
        :title,
        :author,
        :genre,
        :rating,
        :deleted
    );
"""

loan_table = """
    create table if not exists loan (
        loan_id bigserial primary key,
        book_id int not null references book(book_id) on delete cascade,
        user_id int not null references users(user_id) on delete cascade,
        loaned boolean not null default false,
        loan_time timestamp,
        due_date timestamp,
        late_fee boolean not null default false,
        overdue_return bool not null default false
    );
"""

loan_insert = """
    insert into loan (
        book_id,
        user_id,
        accumulated_late_fee,
        loaned,
        loan_time,
        due_date,
        late_fee,
        overdue_return
    ) values (
        :book_id,
        :user_id,
        :accumulated_late_fee,
        :loaned,
        :loan_time,
        :due_date,
        :late_fee,
        :overdue_return
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
