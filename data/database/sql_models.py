users_table = """
    create table if not exists users (
        unique_id bigserial primary key,
        user_id int not null unique,
        first_name text not null,
        last_name text not null,
        email_address text not null,
        phone_number text not null,
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
        deleted
    ) values (
        :user_id,
        :first_name,
        :last_name,
        :email_address,
        :phone_number,
        :deleted
    );
"""

book_table = """
    create table if not exists book (
        unique_id bigserial primary key,
        book_id serial unique not null,
        title text not null,
        author text not null,
        genre text not null,
        rating numeric(2,1) not null check (rating >= 1 and rating <= 5),
        deleted bool not null default false
    );
"""

book_insert = """
    insert into book (
        title,
        author,
        genre,
        rating
    ) values (
        :title,
        :author,
        :genre,
        :rating
    );
"""

loan_table = """
    create table if not exists loan (
        loan_id bigserial primary key,
        book_id int not null,
        user_id int not null,
        loan_time timestamp,
        due_date timestamp,
        late_fee boolean not null default false,
        overdue_return bool not null default false,
        constraint fk_loan_book foreign key (book_id) references book(book_id) on delete restrict,
        constraint fk_loan_user foreign key (user_id) references users(user_id) on delete restrict
    );
"""

loan_insert = """
    insert into loan (
        book_id,
        user_id,
        loan_time,
        due_date
    ) values (
        :book_id,
        :user_id,
        :loan_time,
        :due_date
    );
"""

inventory_table = """
    create table if not exists inventory (
        unique_id bigserial primary key,
        book_id int not null,
        quantity_available int not null check (quantity_available >= 0),
        is_available boolean not null default true,
        constraint fk_inventory_book foreign key (book_id) references book(book_id) on delete restrict
    );
"""

inventory_insert = """
    insert into inventory (
        book_id,
        quantity_available,
        is_available
    ) values (
        :book_id,
        :quantity_available,
        :is_available
    );
"""
