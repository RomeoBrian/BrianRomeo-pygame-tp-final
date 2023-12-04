import pygame as pg
from settings.constantes import open_configs
from models.ui import Ui

class Boton(Ui):
    def __init__(self, pantalla, configs: dict,pos,text_input,image,color,scale = 1):
        super().__init__(pantalla, configs)
        #ui
        self.__text_input = text_input
        self.__text = self.renderizar_texto(self.__text_input,20,color)
        if image != None:
            self.image = pg.transform.scale(image,(int(image.get_width()*scale), int(image.get_height()*scale)))
        else:
            self.image = self.__text
        self.rect = self.image.get_rect(center = pos)
        self.__text_rect = self.__text.get_rect(center = pos)
        self.__clicked = False

    def draw(self,pantalla):
        accion = False
        mouse_pos = pg.mouse.get_pos()
        teclas = pg.key.get_pressed()
    
        if self.rect.collidepoint(mouse_pos):
            if (pg.mouse.get_pressed()[0] == 1 or teclas[pg.K_RETURN] == 1) and not self.__clicked:
                self.__clicked = True
                accion = True
        if pg.mouse.get_pressed()[0] == 0 or teclas[pg.K_RETURN] == 0:
            self.__clicked = False
        
        if self.image is not None:
            pantalla.blit(self.image, self.rect)
        pantalla.blit(self.__text, self.__text_rect)
        #pantalla.blit(self.image, (self.rect.x, self.rect.y))
        
        return accion