import src.services.commands as serv
import src.grid.board as board

class CUI:
    def __init__(self):
        self.__game = serv.Commands()

    def run(self):
        print("Welcome to the game")
        print(self.__game.board)
        while self.__game.status == "in progress":
            command=input("Enter command: ")
            if command == "help":
                print("Commands: fire,cheat,exit")
            elif command == "cheat":
                print(self.__game.cheat_board)
            elif command == "exit":
                break
            elif len(command.split())==2:
                if command.split()[0] != "fire":
                    print("Invalid command")
                    continue
                try:
                    coordinates=command.split()[1]
                    x=coordinates[0]
                    y=int(coordinates[1])
                    hit=self.__game.fire(x,y)
                    if hit==1:
                        print("Congratulations! You hit an alien ship")
                    else:
                        print("U hit void space, but good job")
                except ValueError as ve:
                    print(ve)
                print(self.__game.board)
            else:
                print("Invalid command")
        print("Game over")
        print("Game",self.__game.status)
