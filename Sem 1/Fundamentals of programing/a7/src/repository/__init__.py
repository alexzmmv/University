from src.domain import Book
import pickle
import xml.etree.ElementTree as ET
import sqlite3


ISBN = 0
AUTHOR = 1
TITLE = 2

class MemoryRepository:
    def __init__(self):
        self._books = {}

    def add(self, book_isbn, book_author, book_title):
        if book_isbn in list(self._books.keys()):
            raise ValueError("Book already exists")
        self._books[book_isbn] = Book(book_isbn, book_author, book_title)

    
    def get_all(self):
        return self._books

    def update(self, books, word=None):
        self._books = books.copy()

class FileRepository(MemoryRepository):
    def _load(self):
        self._books = dict()
        try:
            with open(self._file_name, 'r') as file:
                for line in file:
                    isbn, author, title = line.strip().split(',')
                    print(isbn, author, title)
                    super().add(isbn, author, title)
        except EOFError as Error:
            raise ValueError("File error:\n" + str(Error))

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def __save(self):
        with open(self._file_name, 'w') as file:
            for book_key in self._books.keys():
                file.write(book_key + ',' + self._books[book_key].author + ',' + self._books[book_key].title + '\n')

    def add(self, book_isbn, book_author, book_title):
        super().add(book_isbn, book_author, book_title)
        self.__save()

    def update(self, books, word=None):
        super().update(books)
        self.__save()


    def get_all(self):
        return super().get_all()


class BinaryFileRepository(MemoryRepository):
    def _load(self):
        try:
            with open(self._file_name, 'rb') as file:
                self._books = pickle.load(file)
        except EOFError:
            self._books = {}

    def _save(self):
        with open(self._file_name, 'wb') as file:
            pickle.dump(self._books, file)

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, book_isbn, book_author, book_title):
        super().add(book_isbn, book_author, book_title)
        self._save()

    def update(self, books, word=None):
        super().update(books)
        self._save()

    def get_all(self):
        return super().get_all()

class XmlFileRepository(MemoryRepository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, book_isbn, book_author, book_title):
        super().add(book_isbn, book_author, book_title)
        self._save()

    def update(self, books, word=None):
        super().update(books, word)
        self._save()

    def _save(self):
        root = ET.Element("library")

        for isbn, book in self._books.items():
            book_element = ET.SubElement(root, "book", isbn=isbn)
            author_element = ET.SubElement(book_element, "author")
            author_element.text = book.author
            title_element = ET.SubElement(book_element, "title")
            title_element.text = book.title

        tree = ET.ElementTree(root)
        tree.write(self._file_name, encoding="utf-8", xml_declaration=True)

    def _load(self):
        try:
            tree = ET.parse(self._file_name)
            root = tree.getroot()

            for book_element in root.findall("book"):
                isbn = book_element.get("isbn")
                author = book_element.find("author").text
                title = book_element.find("title").text

                self._books[isbn] = Book(isbn, author, title)

        except (ET.ParseError, FileNotFoundError):
            # Ignore errors and start with an empty repository if the file doesn't exist or has incorrect XML format
            pass

class DataBaseRepository(MemoryRepository):
    def _load(self):
        self._connection = sqlite3.connect(self._file_name)
        self._cursor = self._connection.cursor()
        self._cursor.execute("CREATE TABLE IF NOT EXISTS books (isbn TEXT PRIMARY KEY, author TEXT, title TEXT) ")
        self._connection.commit()
        self._cursor.execute("SELECT * FROM books")
        for book in self._cursor.fetchall():
            super().add(book[ISBN], book[AUTHOR], book[TITLE])

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, book_isbn, book_author, book_title):
        super().add(book_isbn, book_author, book_title)
        self._cursor.execute("INSERT INTO books VALUES (?, ?, ?)", (book_isbn, book_author, book_title))
        self._connection.commit()

    def update(self, books, word):
        if word=="sql database":
            super().update(books)
            return
        self._cursor.execute(f"DELETE FROM books WHERE Title LIKE '{word}%';")
        self._connection.commit()
    def get_all(self):
        return super().get_all()

    def close(self):
        self._connection.close()
