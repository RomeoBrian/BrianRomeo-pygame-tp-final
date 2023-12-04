import pygame as pg

class Select_node(pg.sprite.Sprite):
    def __init__(self,pos,estado,velocidad_icono) -> None:
        super().__init__()
        self.image = pg.Surface((300,150))
        if estado == 'desbloqueado':
            self.image.fill('blue')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center = pos)

        #colision
        self.__zona_colision = pg.Rect(self.rect.centerx - (velocidad_icono/2),self.rect.centery - (velocidad_icono/2),velocidad_icono,velocidad_icono)
        


    @property
    def zona_colision(self):
        return self.__zona_colision