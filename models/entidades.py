import pygame as pg

class fisicasEntidades:
    def __init__(self, game, e_type, pos, size):
        self.__game = game
        self.__tipo_entidad = e_type
        self.__posicion = list(pos)
        self.__size = size
        self.__velocidad = [0,0]

    def update(self, movimiento=(0,0)):
        movimiento_frames = (movimiento[0] + self.__velocidad[0], movimiento[1] + self.__velocidad[1])

        self.__posicion[0] += movimiento_frames[0]
        self.__posicion[1] += movimiento_frames[1]
    
    def render(self, surface):
        surface.blit(self.__game.assets['player'], self.__posicion)