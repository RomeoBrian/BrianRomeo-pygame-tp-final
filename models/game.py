import pygame as pg, sys
from settings.constantes import ANCHO,FPS,ALTO,open_configs
from models.nivel import Nivel
from models.ui import Ui
from models.nivel_select import Nivel_select
from models.botones import Boton
from models.menu_opciones import Opciones

class Game:
    
    def __init__(self) -> None:
        self.__nivel_maximo_alcanzado = 2
        self.__config = open_configs()
        self.__niveles = open_configs().get('level_manager_settings')
        self.__estado = 'seleccion'
        self.screen = pg.display.set_mode((ANCHO,ALTO))
        self.surface = pg.Surface((ANCHO,ALTO), pg.SRCALPHA)
        self.__color_fondo = (20, 19, 39,255)
        pg.display.set_caption("Unamed plataformer")
        self.clock = pg.time.Clock()
        self.__nivel_select = Nivel_select(0,self.__nivel_maximo_alcanzado,self.screen,self.crear_nivel)
        #self.__nivel = Nivel(MAP,self.screen,self.__nivel_config,self.ancho_nivel)
        self.fog = pg.Surface((ANCHO,ALTO))
        self.fog.fill((91, 94, 94))
        self.fag_rect = self.fog.get_rect(topleft = (0,0))
        self.__cliked = False

        #pausa
        self.__game_pausa = False
        self.__button_image = pg.image.load(open_configs().get('ui_settings').get('boton')).convert_alpha()
        self.__tiempo_en_pausa = 0
        self.__minutos_en_pausa = 0
        self.__game_minuts_pause = 0
        self.__segundos_en_pausa = 0
        self.__game_seconds_pause = 0
        self.__bandera_pausa_segundos = 0
        self.__bandera_pausa_minutos = 0

        #crear Boton
        self.__boton_resume = Boton(self.screen,self.__config.get('ui_settings'),((ANCHO/2),(ALTO/2) - 90),'SALIR PAUSA',None,'white',0.5)
        self.__boton_opciones = Boton(self.screen,self.__config.get('ui_settings'),((ANCHO/2),(ALTO/2) - 10),'OPCIONES',None,'white',0.5)
        self.__boton_volver = Boton(self.screen,self.__config.get('ui_settings'),((ANCHO/2),(ALTO/2) + 70),'VOLVER AL MENU',None,'white',0.5)
        self.__boton_score = Boton(self.screen,self.__config.get('ui_settings'),((ANCHO - 150),(ALTO - 60)),'MOSTRAR SCORE',None,'white',0.5)

        #tiempo de juego
        self.__time_level_start = pg.time.get_ticks()

        #ui
        self.__ui = Ui(self.screen,self.__config.get('ui_settings'))

        #opciones
        self.__opciones = Opciones(True,self.screen)

    def crear_seleccion_nivel(self,nivel_actual,nuevo_maximo_nivel):
        if nuevo_maximo_nivel > self.__nivel_maximo_alcanzado:
            self.__nivel_maximo_alcanzado = nuevo_maximo_nivel
        self.__nivel_select = Nivel_select(nivel_actual,self.__nivel_maximo_alcanzado,self.screen,self.crear_nivel)
        self.__estado = 'seleccion'
        self.__nivel.main_theme.stop()
        self.__game_pausa = False
    
    def crear_nivel(self,nivel_actual):
        nivel_config = self.__config.get(self.__niveles[nivel_actual]['contenido'])
        self.__nivel = Nivel(self.screen,nivel_config,self.crear_seleccion_nivel,nivel_actual)
        self.__estado = 'nivel'

    def vovler_estado(self,estado):
        self.__estado = estado
    
    def tiempo_trascurrido(self):
        print(self.__tiempo_en_pausa)
        


    def run(self,manejar_estado):
        minutos = 0
        while True:
            touch_space = False
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_ESCAPE:
                        if self.__game_pausa:
                            self.__game_pausa = False
                            #self.__time_level_start = pg.time.get_ticks()
                        else:
                            self.__game_pausa = True
                            self.__game_seconds_pause = segundos_en_milisegundos
                            self.__game_minuts_pause = minutos_en_milisegundos
                            if minutos_en_milisegundos > 0:
                                self.__bandera_pausa_minutos += 1
                            self.__bandera_pausa_segundos += 1
                    if evento.key == pg.K_SPACE:
                        touch_space = True
                if evento.type == pg.MOUSEBUTTONUP:
                    self.__cliked = False
                
                
                    
        
            self.screen.fill(self.__color_fondo)
            #set nivel
            delta_ms = self.clock.tick(FPS)
            
            if self.__estado == 'seleccion':
                self.__ui.dibujar_texto('SELECCION DE NIVEL',50,((ANCHO/2),(ALTO/2) - 300),'white')
                self.__nivel_select.run()
                if self.__boton_score.draw(self.screen) and not self.__cliked:
                            self.__estado = 'score'
                            self.__cliked = True
            if self.__estado == 'score':
                self.__opciones.mostar_higscore(self.vovler_estado,'seleccion')
            elif self.__estado == 'nivel':
                self.__nivel.run(delta_ms,self.__game_pausa,touch_space,minutos)
                self.__ui.mostar_vida(self.__nivel.player.sprite.vidas,self.__nivel.player.sprite.vida_maxima)
                self.__ui.mostrar_fish(self.__nivel.sobrecito_coin)
                if self.__game_pausa:
                    self.__segundos_en_pausa = pg.time.get_ticks() - self.__game_seconds_pause
                    self.__minutos_en_pausa = pg.time.get_ticks() - self.__game_minuts_pause
                    color_fondo_pausa = (20, 19, 39,150)
                    pg.draw.rect(self.surface,color_fondo_pausa,[0,0,ANCHO,ALTO])
                    self.screen.blit(self.surface,(0,0))
                    self.__ui.dibujar_texto('PAUSA',50,((ANCHO/2),(ALTO/2) - 300),'white')
                    if self.__estado == 'nivel':
                        if self.__boton_resume.draw(self.screen) and not self.__cliked:
                            self.__game_pausa = False
                            self.__cliked = True
                        elif self.__boton_opciones.draw(self.screen) and not self.__cliked:
                            self.__estado = 'opciones'
                            self.__cliked = True
                        elif self.__boton_volver.draw(self.screen) and not self.__cliked:
                            self.__nivel.crear_seleccion_nivel(self.__nivel.nivel_actual,self.__nivel_maximo_alcanzado)
                            self.__cliked = True
                    if self.__estado == 'opciones':
                        self.__opciones.menu_opciones(self.vovler_estado,'nivel')
                else:
                    #mostrar tiempo transcurrido de juego
                    segundos_pausa_total = self.__game_seconds_pause + self.__segundos_en_pausa
                    minutos_pausa_total = self.__game_minuts_pause + self.__minutos_en_pausa
                    segundos = int((((pg.time.get_ticks() - self.__time_level_start) if self.__bandera_pausa_segundos < 1 else ((pg.time.get_ticks() - segundos_pausa_total)+ self.__game_seconds_pause)) / 1000) % 60)
                    segundos_en_milisegundos = segundos * 1000
                    minutos = int((((pg.time.get_ticks() - self.__time_level_start) if self.__bandera_pausa_minutos < 1 else ((pg.time.get_ticks() - minutos_pausa_total)+ self.__game_minuts_pause)) / 60000) % 24)
                    minutos_en_milisegundos = minutos * 60000
                    message = f'tiempo: {minutos}:{segundos:02d}'
                    self.__ui.dibujar_texto(message,10,(ANCHO - 80,10),'white')
                
            #self.screen.blit(self.fog,(0,0), special_flags=3)


            pg.display.update()