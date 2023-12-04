import pygame as pg
from settings.constantes import ALTO,ANCHO

class Camara:
    def __init__(self,player):
        self.__player = player
        self.__offset = pg.math.Vector2(0,0)
        self.__offset_float = pg.math.Vector2(0,0)
        self.__ancho_pantalla, self.__alto_pantalla = ALTO,ANCHO
        self.__CONSTANTE = pg.math.Vector2(-self.__ancho_pantalla/2 + player.rect.w/2, -self.__player.direccion.y + 20)

    @property
    def camara_offset(self):
        return self.__offset
    
    def scroll(self):
        self.__offset_float.x += (self.__player.rect.x - self.__offset_float.x + self.__CONSTANTE.x)
        print(self.__offset_float.x)
        self.__offset_float.y += (self.__player.rect.y - self.__offset_float.y + self.__CONSTANTE.y)
        self.__offset.x, self.__offset.x = int(self.__offset_float.x), int(self.__offset_float.y) 
        