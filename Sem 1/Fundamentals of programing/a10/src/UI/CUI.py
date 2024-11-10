SIZEX=0
SIZEY=1
class UI:
    EASY = '1'
    MEDIUM = '2'
    HARD = '3'
    def __init__(self, game):
        self._game = game

    def initBoard(self):
        sizex = input('Number of rows: ')
        sizey = input('Number of columns: ')
        self._game.Set_Board(sizex, sizey)

    def initDifficulty(self):
        while True:
            print('Levels:')
            print('1. Easy')
            print('2. Medium')
            print('3. Hard')
            dificulty_level = input('Difficulty: ')
            if dificulty_level == self.EASY:
                self._game.Set_Computer('Easy')
                break
            elif dificulty_level == self.MEDIUM:
                self._game.Set_Computer('Medium')
                break
            elif dificulty_level == self.HARD:
                self._game.Set_Computer('Hard')
                break
            else:
                print('Invalid difficulty level')
    @staticmethod
    def _readPlayerMove():
        try:
            player_input = input('Place: ').split(' ')
        except Exception as err:
            print(err)
            print('Invalid coordinates')
        return (int(player_input[SIZEX]), int(player_input[SIZEY]))

    def start(self):
        self.initBoard()
        self.initDifficulty()
        board = self._game.board
        playerMove = True
        while not board.is_ended():
            print(board)
            print()
            if playerMove:
                try:
                    move = self._readPlayerMove()
                    self._game.Player_Move(*move)
                except Exception as ex:
                    print(ex)
                    continue
            else:
                self._game.Computer_Move()
            playerMove = not playerMove
            if board.is_ended():
                if playerMove:
                    print("GAME LOST, COMPUTER WON, YOU'RE A LOSER")
                else:
                    print("GAME WON, YOU WON, YOU'RE NOT A LOOSER")
        print(board)