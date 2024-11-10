import texttable as tt
import random as r
LETTERS=['A','B','C','D','E','F','G']
#board is a 7x7 matrix
DX=[-1,0,1,0]
DY=[0,1,0,-1]
class Board:
    @staticmethod
    def init_board():
        board=[[' ']*7 for _ in range(7)]
        board[3][3]='E'
        #asteroid generate
        asteroid_count=0
        coordinate_not_available_list=[(3,3)]
        while asteroid_count<8:
            x=r.randint(0,6)
            y=r.randint(0,6)
            if (x,y) not in coordinate_not_available_list:
                board[x][y]='*'
                for dx in DX:
                    for dy in DY:
                        if 0<=x+dx<=6 and 0<=y+dy<=6:
                            coordinate_not_available_list.append((x+dx,y+dy))
                asteroid_count+=1
        aliendship_count=0
        #generate outer edge list
        outer_edge_list=[]
        for i in range(7):
            outer_edge_list.append((0,i))
            outer_edge_list.append((6,i))
            outer_edge_list.append((i,0))
            outer_edge_list.append((i,6))
        while aliendship_count<2:
            i,j=r.choice(outer_edge_list)
            if board[i][j]==' ':
                board[i][j]='X'
                aliendship_count+=1


        return board
    def __init__(self):
        self.__board=self.init_board()

    @property
    def cheat_board(self):
        t=tt.Texttable()
        row=[' ','A','B','C','D','E','F','G']
        t.add_row(row)
        for i in range(7):
            row=[' ']*8
            for j in range(8):
                if j == 0:
                    row[0]=i+1
                    continue
                if self.__board[i][j-1] == 'E':
                    row[j]='E'
                elif self.__board[i][j-1]=='*':
                    row[j]='*'
                elif self.__board[i][j-1]=='X':
                    row[j]='X'
                elif self.__board[i][j-1]=='-':
                    row[j]='-'
                else:
                    row[j]=' '
            t.add_row(row)
        return t.draw()
    def move_alien_ship(self):
        coordinate_list=[]
        for i in range(7):
            for j in range(7):
                if self.__board[i][j]=='X':
                    coordinate_list.append((i,j))
                    self.__board[i][j]=' '
        choices=['closer','same distance']
        outer_edge_list=[]
        for i in range(7):
            outer_edge_list.append((0,i))
            outer_edge_list.append((6,i))
            outer_edge_list.append((i,0))
            outer_edge_list.append((i,6))
        midle_edge_list=[]
        for i in range(1,6):
            midle_edge_list.append((1,i))
            midle_edge_list.append((5,i))
            midle_edge_list.append((i,1))
            midle_edge_list.append((i,5))
        close_edge_list=[]
        for i in range(2,5):
            close_edge_list.append((2,i))
            close_edge_list.append((5,i))
            close_edge_list.append((i,2))
            close_edge_list.append((i,5))
        outer_edge_list=list(set(outer_edge_list))
        midle_edge_list=list(set(midle_edge_list))
        close_edge_list=list(set(close_edge_list))
        for i,j in coordinate_list:
            choice=r.choice(choices)
            if choice=='same distance':
                    if (i,j) in outer_edge_list:
                        while True:
                            c=r.choice(outer_edge_list)
                            if self.__board[c[0]][c[1]]==' ':
                                self.__board[c[0]][c[1]]='X'
                                break
                    if (i,j) in midle_edge_list:
                        while True:
                            c=r.choice(midle_edge_list)
                            if self.__board[c[0]][c[1]]==' ':
                                self.__board[c[0]][c[1]]='X'
                                break
            else:
                if choice=='closer':
                    if (i,j) in outer_edge_list:
                        while True:
                            c=r.choice(midle_edge_list)
                            if self.__board[c[0]][c[1]]==' ':
                                self.__board[c[0]][c[1]]='X'
                                break

                    if (i,j) in midle_edge_list:
                        while True:
                            c=r.choice(close_edge_list)
                            if self.__board[c[0]][c[1]]==' ':
                                self.__board[c[0]][c[1]]='X'
                                break


    def fire(self,x,y):
        """
        :param first coordinate:
        :param y: second coordinate
        :return:
        1 if it hit a alien ship
        0 if it didn't hit a alien ship
        """
        if (x not in LETTERS) or (y not in range(1,8)) or isinstance(x,str)==False or isinstance(y,int)==False:
            raise ValueError('Invalid coordinates')
        x=ord(x)-ord('A')
        y=y-1
        x,y=y,x
        print(f"x={x},y={y}")
        print(self.__board[x][y])
        if y==3 and x==3:
            raise ValueError('this is earth y dumb')
        if self.__board[x][y]=='*':
            raise ValueError('this is an asteroid y dumb')
        if self.__board[x][y]=='-':
            raise ValueError('this is already fired')

        if self.__board[x][y]=='X':
            self.__board[x][y]='-'

            return 1
        if self.__board[x][y]==' ':
            self.__board[x][y]='-'
            self.move_alien_ship()
            return 0

    def game_status(self):
        """
        :return:
        "Win" if the game is won
        "Lost" if the game is not won
        "waiting" if the game is still going
        """
        for i in DX:
            for j in DY:
                if 0<=3+i<=6 and 0<=3+j<=6:
                    if self.__board[3+i][3+j]=='X':
                        return 'Lost'
        for i in range(7):
            for j in range(7):
                if self.__board[i][j]=='X':
                    return "in progress"
        return "win"

    def __str__(self):
        t=tt.Texttable()
        row=[' ','A','B','C','D','E','F','G']
        t.add_row(row)
        for i in range(7):
            row=[' ']*8
            for j in range(8):
                if j == 0:
                    row[0]=i+1
                    continue
                if self.__board[i][j-1] == 'E':
                    row[j]='E'
                elif self.__board[i][j-1]=='*':
                    row[j]='*'
                elif self.__board[i][j-1]=='-':
                    row[j]='-'
                else:
                    row[j]=' '
            t.add_row(row)
        return t.draw()