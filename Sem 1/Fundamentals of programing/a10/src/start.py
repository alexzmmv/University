from src.UI.CUI import UI
from services.services import Game, read_settings


def start():
    game = Game()
    settings = read_settings()
    if settings['user_interface'] == 'Console':
        ui = UI(game)
    elif settings['user_interface'] == 'Graphical':
        ui = GUI(game)
    else:
        print('Invalid user interface, check settings file and try again')
    ui.start()

start()
