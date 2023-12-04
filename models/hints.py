import pygame as pg
from settings.constantes import open_configs
from models.boundries import Boundry
from models.ui import Ui

class Hint(Boundry):
    def __init__(self, pos, size,pantalla,mensaje = None,imagen=None):
        super().__init__(pos, size, imagen)
        self.__mensaje = mensaje
        #ui
        self.__ui = Ui(pantalla,open_configs().get('ui_settings'))

    
    def imprimir_mensaje(self):
        if self.__mensaje is not None:
            self.__ui.dubijar_texto_doble_linea(self.__mensaje,(self.rect.centerx,self.rect.centery),10,'white')
    
    def update(self, mover):
        self.imprimir_mensaje()
        return super().update(mover)
        