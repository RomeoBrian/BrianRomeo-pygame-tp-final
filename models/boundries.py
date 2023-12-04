import pygame as pg

class Boundry(pg.sprite.Sprite):
    def __init__(self,pos,size,imagen = None): 
        super().__init__()
        if imagen == None:
            self.image = pg.Surface((size,size)).convert_alpha()
            self.image.fill((255,255,255,0))
        else:
            self.image = pg.image.load(imagen)
            self.image = pg.transform.scale(self.image,(size,size))
        #self.image.set_alpha(128)
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, mover):
        self.rect.x += mover