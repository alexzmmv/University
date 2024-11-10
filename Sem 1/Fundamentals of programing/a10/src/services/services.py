from src.board.board import Board
from src.services.Computer_AI import *


class Game:
    def __init__(self, board=None, computer_player=None):
        self._board = board
        self._computerPlayer = computer_player

    @property
    def board(self):
        return self._board

    def Player_Move(self, x, y):
        self._board.move(x, y, 'X')

    def Computer_Move(self):
        move = self._computerPlayer.calculateMove(self._board)
        self._board.move(move[0], move[1], '0')

    def Set_Board(self, x, y):
        self._board = Board(x, y)

    def Set_Computer(self, difficulty):
        if difficulty == 'Hard':
            self._computerPlayer = SmartestComputer()
        elif difficulty == 'Medium':
            self._computerPlayer = RandomComputer()
        elif difficulty == 'Easy':
            self._computerPlayer = EasyComputer()

    def __str__(self):
        return str(self._board)


def read_settings():
    settings = {}
    with open("../src/!settings.properties", 'r') as file:
        for line in file:
            # Skip comments and empty lines
            if not line.strip() or line.strip().startswith('#'):
                continue
            key, value = line.strip().split('=')
            settings[key.strip()] = value.strip()
    return settings
