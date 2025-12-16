from data.classes.book import Book


def testing_repr() -> Book:
    b = Book("test", "test", "test", 0.0)
    return b


def main():
    print(testing_repr())


if __name__ == "__main__":
    main()
