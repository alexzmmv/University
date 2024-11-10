class Person:
    def __init__(self, id, name, phone_number):
        if not isinstance(id, int):
            raise ValueError("id must be an integer")
        self.__id = id
        self.name = name
        self.phone_number = phone_number

    @property
    def id(self):
        return self.__id

    def update(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
    def __str__(self):
        return str(self.__id) + " " + self.name + " " + self.phone_number

    def __deepcopy__(self, memodict={}):
        return Person(self.__id, self.name, self.phone_number)