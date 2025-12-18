from data.classes.book import Book
from data.classes.user import User

def two_csutomer_loan_a_booK() -> NOne:  
    cust1 = User("test", "test", "test@test.test.test", "012345678")
    cust2 = User("test1", "test1", "test1@test.test.test", "123456789")
    
   
book1 = Book("test", "test", "test", 0.0)



def testing_repr() -> Book:
    b = Book("test", "test", "test", 0.0)
    return b


def main():
    print(testing_repr())


if __name__ == "__main__":
    main()

'''
write some code that allows you to instantiate two users that each loan out one book both return their books.
'''