class User:

    def __init__(self, name, email):  # name is string \\ email is string
        self.name = name
        self.email = email
        self.books = {}  # {BOOK:rating}

    def __repr__(self):
        return 'User {name}, email: {email}, books read: {num}'.format(name=self.name, email=self.email,
                                                                       num=len(self.books))

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print('Email Updated... ')
        return self.email

    def read_book(self, book, rating=None):  # Book should be an Object
        self.books[book] = rating

    def get_average_rating(self):
        lst_of_ratings = [y for x, y in self.books.items()]
        lst_of_ratings = [x for x in lst_of_ratings if x is not None]
        if len(lst_of_ratings) >= 1:
            return sum(lst_of_ratings) / len(lst_of_ratings)


class Book:

    def __init__(self, title, isbn, price=None):  # title is string \\ isbn is number
        self.title = title
        self.isbn = isbn
        self.rating = []
        self.price = price

    def __repr__(self):
        return '{title}: {isbn}'.format(title=self.title, isbn=self.isbn)

    def __eq__(self, other):
        return self.title == other.title and self.isbn == other.isbn

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print('ISBN Updated...')
        return self.isbn

    def add_rating(self, rating):  # Added float numbers for ratings to give more variety of rating
        a = [i * .1 for i in range(0, 41)]
        b = [round(i, 2) for i in a]  # rounding numbers to 0.00
        if rating in b:
            self.rating.append(rating)
        else:
            print('Invalid Rating')
        # return self.rating

    def get_average_rating(self):
        return sum(self.rating) / len(self.rating)


class Fiction(Book):

    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return '{title} by {author}'.format(title=self.title, author=self.author)


class Non_Fiction(Book):

    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject  # String
        self.level = level  # String

    def __repr__(self):
        return '{title}, a {level} manual on {subject}'.format(title=self.title,
                                                               level=self.level,
                                                               subject=self.subject)

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level


class TomeRater:

    def __init__(self):
        self.user = {}  # Map USERS email to corresponding User Object {'D@gmail.com, USER}
        self.books = {}  # Map a BOOK Object to the number of Users that have read it
        # {BOOK:,(Num of Users that read it)}

    # def __repr__(self):
    #     return ('TomeRater Initialized')

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.user:
            print('No USER with email {email}'.format(email=email))
        else:
            print('Added {book}'.format(book=book))
            self.user[email].read_book(book, rating)  # Book should be object \\ adds BOOK to books for user
            if rating:
                book.add_rating(rating)

        if book not in self.books:
            self.books[book] = 1
        else:
            self.books[book] += 1

    def add_user(self, name, email, user_books=None):  # user_books is a list
        email_ending = ['.com', '.edu', '.org']
        if email in self.user:
            print("User '{user}' already Exists! ".format(user=name))
        if email[-4:] not in email_ending:
            print("INVALID EMAIL '{}', must end with {}".format(email, email_ending))
        else:
            self.user[email] = User(name, email)
            print('User {user} added! '.format(user=name))
        if user_books:
            for book in user_books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.user.values():
            print(user)

    def get_most_read_book(self):
        total = max(self.books.values())
        book_list = [str(book) for book, number_of_books in self.books.items() if number_of_books == total]
        if len(book_list) > 1:
            return "\n".join(book_list) + "\nEach read {times_read} times!".format(times_read=total)
        return '{book} was read {total} times'.format(book=book_list[0], total=total)

    def highest_rated_book(self):
        total = 0
        for book, number_of_books in self.books.items():
            if book.get_average_rating() > total:
                total = book.get_average_rating()
        lst = [str(book) for book, value in self.books.items() if book.get_average_rating() == total]
        if len(lst) > 1:
            return "\n".join(lst) + "\nWith an average review of {average_review}!".format(average_review=total)
        return '{book} with a rating of {total}!'.format(book=lst[0], total=total)

    def most_positive_user(self):
        rating = [user.get_average_rating() for email, user in self.user.items()]  # User is Object
        rating = [i for i in rating if i is not None]
        most_positive = [str(user) for email, user in self.user.items() if user.get_average_rating() == max(rating)]
        if len(most_positive) > 1:
            return 'The most positive users are:\n' + '\n'.join(most_positive) + '\nWith an average review of {rating}' \
                .format(rating=max(rating))
        return most_positive[0]

    def get_n_most_read_books(self, n):
        # takes in number N and returns the N books that have been read most in descending order
        # returns books in descending order of amount read
        number_books_read = list(self.books.values())
        number_books_read.sort()
        number_books_read = number_books_read[::-1]  # reversing order
        for number in number_books_read:  # removing duplicates
            if number_books_read.count(number) > 1:
                number_books_read.remove(number)
        lst = []
        for i in range(len(number_books_read)):
            for key, value in self.books.items():
                if number_books_read[i] == value:
                    lst.append(str(key) + ': Read {total} times'.format(total=value))
        lst = lst[:n]
        return '\n'.join(lst)


