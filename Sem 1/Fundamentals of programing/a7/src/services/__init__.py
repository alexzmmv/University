from src.repository import MemoryRepository, FileRepository, BinaryFileRepository, XmlFileRepository, DataBaseRepository
from copy import deepcopy


class Services:
    def __read_settings(self):
        settings = {}
        with open("../Data/settings.properties", 'r') as file:
            for line in file:
                # Skip comments and empty lines
                if not line.strip() or line.strip().startswith('#'):
                    continue
                key, value = line.strip().split('=')
                settings[key.strip()] = value.strip()
        return settings

    def __init__(self, repository_type=None, repository_path=None):
        self._history = []
        if repository_type is not None and repository_path is not None:
            try:
                settings = self.__read_settings()
                repository_type = settings['repository']
                repository_path = settings['path']
            except KeyError:
                raise ValueError("Invalid settings file")
        else:
            repository_type = repository_type
            repository_path = repository_path
        try:
            if repository_type == 'Memory':
                self._repository = MemoryRepository()
            elif repository_type == 'TextFile':
                self._repository = FileRepository(repository_path)
            elif repository_type == 'BinaryFile':
                self._repository = BinaryFileRepository(repository_path)
            elif repository_type == 'XmlFile':
                self._repository = XmlFileRepository(repository_path)
            elif repository_type == 'DataBase':
                self._repository = DataBaseRepository(repository_path)
            else:
                raise ValueError("Invalid repository type")
        except ValueError as Error:
            raise ValueError("Services Error:\n" + str(Error))
        self._history.append(deepcopy(self._repository.get_all()))
        self.__original_books = deepcopy(self._repository.get_all())

    def add_book(self, book_isbn, book_author, book_title):
        self._repository.add(book_isbn, book_author, book_title)
        self._history.append(deepcopy(self._repository.get_all()))

    def filter_books(self, word):
        books = self._repository.get_all()
        for book_key in list(books.keys()):
            book = books[book_key]
            if word == book.title.split()[0]:
                del books[book_key]
        self._repository.update(books, word)
        self._history.append(deepcopy(self._repository.get_all()))

    def undo(self):
        if len(self._history) == 1:
            raise ValueError("No more undo operations")

        self._history.pop()
        self._repository.update(self._history[-1], "sql database")

    def get_books_string(self):
        books = self._repository.get_all()
        string = ""
        for book_key in books.keys():
            string += str(books[book_key]) + "\n"
        return string
