import pygame as pg
import random

class Tile(pg.sprite.Sprite):
    def __init__(self,pos,size,tile_list,is_movable = False, direccion_x = False,direccion_y = False): 
        super().__init__()
        #self.image = pg.Surface((size,size))
        self.__posicion_inicial = (pos)
        self.__tile_list = tile_list
        self.image = pg.image.load(self.__tile_list[0])
        self.image = pg.transform.scale(self.image,(size,size))
        #self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)
        
        #movimiento tiles
        self.__is_movable = is_movable
        self.__direccion_x = direccion_x
        self.__direccion_y = direccion_y
        self.__direccion_movimiento = pg.math.Vector2(1,1)
        self.__distancia_recorrida = 128
        self.__frame_movimiento = 0

    @property
    def is_movable(self):
        return self.__is_movable

    def movimiento_tile(self):
        if self.__is_movable and self.__direccion_movimiento:
                self.rect.y += self.__direccion_movimiento.y 
                self.__frame_movimiento += 1
                if self.__frame_movimiento > self.__distancia_recorrida:
                    self.__direccion_movimiento.y *= -1
                    self.__frame_movimiento = 0

    def update(self, mover):
        self.rect.x += mover
        self.movimiento_tile()