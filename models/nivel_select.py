import pygame as pg
from settings.constantes import open_configs
from models.select_node import Select_node
from models.icons import Icon

class Nivel_select():
    def __init__(self,primer_nivel,ultimo_nivel,pantalla,crear_nivel) -> None:
        self.__pantalla = pantalla
        self.__nivel_actual = primer_nivel
        self.__ultimo_nivel = ultimo_nivel
        self.__level_manager_settings = open_configs().get('level_manager_settings')
        self.__crear_nivel = crear_nivel
        
        #movimiento
        self.__moviendose = False
        self.__direccion_movimiento = pg.math.Vector2(0,0)
        self.__velocidad_movimiento = 8
        
        #sprites
        self.niveles_setup()
        self.player_icono_setup()
        
        

        

    def niveles_setup(self):
        self.__nodo = pg.sprite.Group()

        for index,niveles in enumerate(self.__level_manager_settings):
            if index <= self.__ultimo_nivel:
                sprite_nodo = Select_node(niveles['pos'],'desbloqueado',self.__velocidad_movimiento)
            else:
                sprite_nodo = Select_node(niveles['pos'],'bloqueado',self.__velocidad_movimiento)
            self.__nodo.add(sprite_nodo)
    
    def dibujar_ruta(self):
        if self.__ultimo_nivel > 0:
            puntos = [niveles['pos'] for index,niveles in enumerate(self.__level_manager_settings) if index <= self.__ultimo_nivel]
            pg.draw.lines(self.__pantalla,'skyblue',False,puntos,6)
                
    def player_icono_setup(self):
        self.__player_icono = pg.sprite.GroupSingle()
        player_icono_sprite = Icon(self.__nodo.sprites()[self.__nivel_actual].rect.center)
        self.__player_icono.add(player_icono_sprite)

    def movimiento(self):
        tecla = pg.key.get_pressed()
        
        if not self.__moviendose:
            if tecla[pg.K_d] and self.__nivel_actual < self.__ultimo_nivel:
                self.__direccion_movimiento = self.datos_movimiento('siguiente')
                #print(self.__direccion_movimiento)
                self.__nivel_actual += 1
                self.__moviendose = True
            elif tecla[pg.K_a] and self.__nivel_actual > 0:
                self.__direccion_movimiento = self.datos_movimiento('anterior')
                self.__nivel_actual -= 1
                self.__moviendose = True
            elif tecla[pg.K_SPACE]:
                self.__crear_nivel(self.__nivel_actual)
    
    def datos_movimiento(self,objetivo):
        inicio = pg.math.Vector2(self.__nodo.sprites()[self.__nivel_actual].rect.center)
        if objetivo == 'siguiente':
            fin = pg.math.Vector2(self.__nodo.sprites()[self.__nivel_actual + 1].rect.center)
        else:
            fin = pg.math.Vector2(self.__nodo.sprites()[self.__nivel_actual - 1].rect.center)
        
        return (fin - inicio)

    def update_player_icon(self):
        if self.__moviendose and self.__direccion_movimiento:
            self.__player_icono.sprite.posicion += self.__direccion_movimiento * (self.__velocidad_movimiento/200)
            nodo_objetivo = self.__nodo.sprites()[self.__nivel_actual]
            pg.draw.rect(self.__pantalla,'white',nodo_objetivo.zona_colision)
            if nodo_objetivo.zona_colision.collidepoint(self.__player_icono.sprite.posicion):
                self.__moviendose = False
                self.__direccion_movimiento = pg.math.Vector2(0,0)

    def run(self):
        self.movimiento()
        self.dibujar_ruta()
        self.__nodo.draw(self.__pantalla)
        self.__player_icono.draw(self.__pantalla)
        self.update_player_icon()
        self.__player_icono.update()

        
