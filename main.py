from data.classes import Book


def testing_repr() -> Book:
    """Just figuring out how it works exactly - I can't actually remember if Michael wrote this book lol but anywho"""
    b = Book(1, "War Horse", "Michael Morpurgo", "history", 5)
    return b


def main():
    print(testing_repr())


if __name__ == "__main__":
    main()
