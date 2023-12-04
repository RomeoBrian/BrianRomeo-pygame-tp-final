import pygame as pg
from models.main_menu import Main_menu
from models.game import Game

class State_handler():
    def __init__(self) -> None:
        self.__menu_state = 'main_menu'

    @property
    def menu_state(self):
        return self.__menu_state
    
    def menu_principal(self):
        menu = Main_menu()
        menu.run(self.manejar_estado)
    
    def iniciar_juego(self):
        game = Game()
        game.run(self.manejar_estado)

    def manejar_estado(self, estado = None):
        if estado != None:
            self.__menu_state = estado

        match self.__menu_state:
            case 'main_menu':
                self.menu_principal()
            case 'game':
                self.iniciar_juego()