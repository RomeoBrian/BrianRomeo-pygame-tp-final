import pygame as pg
from models.tiles import Tile

class Trampa(Tile):
    def __init__(self, pos, size, tile_list):
        super().__init__(pos, size, tile_list)
        self.__tile_list = tile_list
        self.image = pg.image.load(self.__tile_list[0])
        self.image = pg.transform.scale(self.image,(size,size))
        self.rect = self.image.get_rect(topleft = pos)
        self.rect.width = 20
        self.rect.height = 20
        self.__contacto = False
        self.__damage_cooldown = 2000
        self.__ready = True

    @property
    def contacto(self):
        return self.__contacto
    @contacto.setter
    def contacto(self,is_true):
        self.__contacto = is_true
    
    @property
    def damage_rect(self):
        return self.__damage_rect
    @damage_rect.setter
    def damage_rect(self,damage):
        self.__damage_rect = damage
    
    def do_damage(self):
        if self.__contacto and self.__ready :
            damage = 20
            self.__ready = False
            self.__tiempo_damage = pg.time.get_ticks()
        else:
            damage = 0
        return damage
    
    def cooldown(self):
        if not self.__ready:
            self.__contacto = False
            curent_time = pg.time.get_ticks()
            if curent_time - self.__tiempo_damage >= self.__damage_cooldown:
                self.__ready = True
    
    def update(self, mover):
        self.cooldown()
        return super().update(mover)

