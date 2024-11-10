from src.services import Services

EXIT = '0'
ADD_BOOK = '1'
DISPLAY_BOOKS = '2'
FILTER_BOOKS = '3'
UNDO = '4'


class UI:
    def __init__(self):
        print("Starting UI...")
        try:
            self._services = Services()
        except ValueError as Error:
            print("Services error:\n" + str(Error))

    def run(self):
        print("1. Add a book")
        print("2. Display the list of books")
        print("3. Filter the list so that book titles starting with a given word are deleted from the list")
        print("4. Undo the last operation that modified program data")
        print("0. Exit")
        while True:
            command = input("Enter command: ")
            if command == ADD_BOOK:
                print("Enter book details:")
                isbn = input("ISBN: ")
                author = input("Author: ")
                title = input("Title: ")
                try:
                    self._services.add_book(isbn, author, title)
                except ValueError as Error:
                    print("Services error: " + str(Error))

            elif command == DISPLAY_BOOKS:
                books_string_representation = self._services.get_books_string()
                print(books_string_representation)
            elif command == FILTER_BOOKS:
                word = input("Enter word to delete all books starting with it: ")
                try:
                    self._services.filter_books(word)
                except ValueError as Error:
                    print("UI Error:\n" + str(Error))
            elif command == UNDO:
                try:
                    self._services.undo()
                except ValueError as Error:
                    print("UI Error:\n" + str(Error))
            elif command == EXIT:
                break
            else:
                print("Invalid command")
        print("Exiting UI...")


UI = UI()
UI.run()
