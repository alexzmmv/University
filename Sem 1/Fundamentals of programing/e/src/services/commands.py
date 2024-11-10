from src.grid.board import Board

class Commands:
    def __init__(self):
        self.__board = Board()

    def get_board(self):
        return self.__board.board
    @property
    def cheat_board(self):
        return self.__board.cheat_board

    def fire(self, x, y):
        return self.__board.fire(x, y)
    @property
    def board(self):
        return self.__board.__str__()

    @property
    def status(self):
        return self.__board.game_status()
