import unittest
from unittest.mock import patch
from src.services import Services
from src.domain import Book

class TestAddBook(unittest.TestCase):
    def test_add_book(self):
        # Test case to ensure that adding a book updates the repository correctly.

        # Arrange
        services = Services(repository_type='Memory')
        book_isbn = "1234567890"
        book_author = "Author"
        book_title = "Title"

        # Act
        services.add_book(book_isbn, book_author, book_title)

        # Assert
        self.assertTrue(book_isbn in services._repository.get_all())
        self.assertEqual(services._repository.get_all()[book_isbn], Book(book_isbn, book_author, book_title))

    def test_add_duplicate_book(self):
        # Test case to ensure that adding a duplicate book raises a ValueError.

        # Arrange
        services = Services(repository_type='Memory')
        book_isbn = "1234567890"
        book_author = "Author"
        book_title = "Title"
        services.add_book(book_isbn, book_author, book_title)  # Add the book once

        # Act & Assert
        with self.assertRaises(ValueError):
            services.add_book(book_isbn, book_author, book_title)  # Attempt to add the same book again

    def test_add_book_invalid_isbn(self):
        # Test case to ensure that adding a book with an invalid ISBN raises a ValueError.

        # Arrange
        services = Services(repository_type='Memory')
        book_isbn = "invalid_isbn"
        book_author = "Author"
        book_title = "Title"

        # Act & Assert
        with self.assertRaises(ValueError):
            services.add_book(book_isbn, book_author, book_title)

if __name__ == '__main__':
    unittest.main()
