from texttable import Texttable
from copy import deepcopy


class Board:
    def __init__(self, sizex, sizey):

        self._size_of_x = int(sizex)
        self._size_of_y = int(sizey)
        self._data = [0] * (self._size_of_x * self._size_of_y)
        self._number_of_moves = 0
        self._number_of_x = 0
        self._number_of_o = 0
        self._history = []

    def move(self, x, y, symbol):
        if x not in range(self._size_of_x) or y not in range(self._size_of_y):
            raise ValueError('Invalid move, coordinates out of bounds')

        if symbol not in ['X', '0']:
            raise ValueError('Invalid symbol')

        if self._data[self._size_of_y * x + y] != 0:
            raise ValueError('Cannot place element')

        self._history.append((
            deepcopy(self._data),
            deepcopy(self._number_of_moves),
            deepcopy(self._number_of_x),
            deepcopy(self._number_of_o)
        ))

        if symbol == 'X':
            self._number_of_x += 1
        else:
            self._number_of_o += 1

        d = {'X': 1, '0': -1}
        loc = self._size_of_y * x + y
        self._data[loc] = d[symbol]
        self._number_of_moves += 1

        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]

        for i in range(8):
            if (
                x + dx[i] in range(self._size_of_x)
                and y + dy[i] in range(self._size_of_y)
                and self._data[self._size_of_y * (x + dx[i]) + y + dy[i]] == 0
            ):
                self._data[self._size_of_y * (x + dx[i]) + y + dy[i]] = 2
                self._number_of_moves += 1

    def is_ended(self):
        return self._number_of_moves == self._size_of_x * self._size_of_y

    def get(self, x, y):
        return self._data[self._size_of_y * x + y]

    def compute_nearby_positions(self, x, y):
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        nr = 0

        for i in range(8):
            if x + dx[i] in range(self._size_of_x) and y + dy[i] in range(self._size_of_y) and self._data[self._size_of_y * (x + dx[i]) + y + dy[i]] == 0:
                nr += 1
        return nr

    def evaluate(self):
        if self.is_ended():
            return 999

        if self._size_of_y * self._size_of_x - self._number_of_moves <= 9:
            if self._number_of_x == self._number_of_o:
                return 10 - (self._size_of_y * self._size_of_x - self._number_of_moves)
            else:
                return -10 + (self._size_of_y * self._size_of_x - self._number_of_moves)

        return 998

    DATA=0
    NUMBER_OF_MOVES=1
    NUMBER_OF_X=2
    NUMBER_OF_O=3

    def undo_for_ai(self):
        save = deepcopy(self._history.pop())
        self._data.clear()
        self._data=save[self.DATA]
        self._number_of_moves = save[self.NUMBER_OF_MOVES]
        self._number_of_x = save[self.NUMBER_OF_X]
        self._number_of_o = save[self.NUMBER_OF_O]

    @property
    def size_of_x(self):
        return self._size_of_x

    @property
    def size_of_y(self):
        return self._size_of_y

    def __str__(self):
        table = Texttable()
        d = {1: 'X', -1: '0', 0: ' ', 2: 'B'}

        for i in range(0, self._size_of_x * self._size_of_y, self._size_of_y):
            row = self._data[i:i + self._size_of_y]
            for j in range(self._size_of_y):
                row[j] = d[row[j]]
            table.add_row(row)

        return table.draw()
