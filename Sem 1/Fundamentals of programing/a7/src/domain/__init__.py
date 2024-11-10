class Book:
    def __init__(self, isbn, author, title):
        self.author = author
        self.title = title
        try:
            self.isbn = int(isbn)
        except ValueError:
            raise ValueError("ISBN must be an integer")

    def __str__(self):
        return f"ISBN: {self.isbn}, Author: {self.author}, Title: {self.title}"

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False

    def __ne__(self, other):
        return not self == other
