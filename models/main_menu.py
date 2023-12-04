import pygame as pg, sys
from settings.constantes import ALTO,ANCHO,FPS,open_configs
from models.botones import Boton
from models.ui  import Ui
from models.menu_opciones import Opciones


class Main_menu():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((ANCHO,ALTO))
        self.__config = open_configs()
        self.__button_image = pg.image.load(open_configs().get('ui_settings').get('boton')).convert_alpha()
        #crear Boton
        self.__boton_start = Boton(self.screen,self.__config.get('ui_settings'),((ANCHO/2),(ALTO/2) - 90),'START',None,'white',0.5)
        self.__boton_opciones = Boton(self.screen,self.__config.get('ui_settings'),((ANCHO/2),(ALTO/2) - 10),'OPCIONES',None,'white',0.5)
        self.__boton_salir = Boton(self.screen,self.__config.get('ui_settings'),((ANCHO/2),(ALTO/2) + 70),'SALIR',None,'white',0.5)
        self.clock = pg.time.Clock()
        self.__estado = 'main'
        self.__clicked = False

        #ui
        self.__ui = Ui(self.screen,self.__config.get('ui_settings'))

        #opciones
        self.__opciones = Opciones(True,self.screen)
    
    def vovler_estado(self,estado):
        self.__estado = estado

    def run(self,manejar_estado):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if evento.type == pg.MOUSEBUTTONUP:
                    self.__clicked = False
            
            self.screen.fill((20, 19, 39,0))
            self.clock.tick(FPS)
            if self.__estado == 'opciones':
                    self.__opciones.menu_opciones(self.vovler_estado,'main')
            if self.__estado == 'name_imput':
                    self.__opciones.pantalla_ingreso_nombre(manejar_estado)
            if self.__estado == 'main':
                self.__ui.dibujar_texto('Menu principal',50,((ANCHO/2),(ALTO/2) - 300),'white')
                if self.__boton_start.draw(self.screen) and not self.__clicked:
                    #manejar_estado('game')
                    self.__estado = 'name_imput'
                    self.__clicked = True
                elif self.__boton_opciones.draw(self.screen) and not self.__clicked:
                    self.__estado = 'opciones'
                    self.__clicked = True
                elif self.__boton_salir.draw(self.screen) and not self.__clicked:
                    self.__clicked = True
                    pg.quit()
                    sys.exit()
                    
        

            pg.display.update()