import pygame as pg

class Icon(pg.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        self.__posicion = pos
        self.image = pg.Surface((32,32))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)

    
    @property
    def posicion(self):
        return self.__posicion
    @posicion.setter
    def posicion(self,pos):
        self.__posicion = pos
    
    def update(self) -> None:
        self.rect.center = self.__posicion