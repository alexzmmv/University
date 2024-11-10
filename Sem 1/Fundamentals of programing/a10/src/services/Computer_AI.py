import random
from copy import deepcopy


class EasyComputer:
    """
    Computer for easy difficulty
    """
    @staticmethod
    def calculateMove(board):
        for i in range(board.size_of_x):
            for j in range(board.size_of_y):
                if board.get(i, j) == 0:
                    return (i, j)


class RandomComputer:
    '''
    Computer for medium difficulty
    '''
    @staticmethod
    def calculateMove(board):
        candidates = []
        for i in range(board.size_of_x):
            for j in range(board.size_of_y):
                if board.get(i, j) == 0:
                    candidates.append((i, j))
        return random.choice(candidates)


class SmartestComputer:
    '''
    Computer for hard difficulty
    '''

    def minmax(self, board, depth, isMax, alpha, beta):
        evaluation_of_board = board.evaluate()
        #if game is finished or game is ongoing
        if evaluation_of_board != 999 and evaluation_of_board != 998:
            return evaluation_of_board

        if board.is_ended():
            return 0
        if beta <= alpha:
            return 0
        if isMax:
            for i in range(board.size_of_x):
                for j in range(board.size_of_y):
                    if board.get(i, j) == 0:
                        board.move(i, j, 'X')
                        alpha = max(alpha, self.minmax(
                            board, depth + 1, not isMax, alpha, beta))
                        board.undo_for_ai()
            return alpha
        else:
            for i in range(board.size_of_x):
                for j in range(board.size_of_y):
                    if board.get(i, j) == 0:
                        board.move(i, j, '0')
                        beta = min(beta, self.minmax(
                            board, depth + 1, not isMax, alpha, beta))
                        board.undo_for_ai()
            return beta

    def calculateMove(self, board):
        bestVal = -1000
        x = -1
        y = -1
        board = deepcopy(board)
        for i in range(board.size_of_x):
            for j in range(board.size_of_y):
                if board.get(i, j) == 0:
                    board.move(i, j, 'X')
                    moveVal = self.minmax(board, 0, False, -1000, 1000)
                    board.undo_for_ai()
                    if moveVal > bestVal:
                        x = i
                        y = j
                        bestVal = moveVal
        return (x, y)