import pygame as pg
from settings.constantes import ANCHO
from settings.utils import importar_carpeta
import random
from models.proyectil import Proyectil


class Enemy(pg.sprite.Sprite):
    def __init__(self,pos,gravedad,enemy_configs: dict):
        super().__init__()
        self.__enemy_configs = enemy_configs
        #path random, entre los enemigos seteados
        #self.__path_random = random.choices(self.__enemy_configs.get('path'),self.__enemy_configs.get('weights'))[0]
        self.importar_enemy_assest()
        #animacion
        self.__frame_index = 0
        self.__frame_rate = self.__enemy_configs.get('frame_rate')
        self.__velocidad_animacion = self.__enemy_configs.get('velocidad_animacion')
        self.__velocidad_movimiento = self.__enemy_configs.get('velocidad_movimiento')
        self.image = self.__animaciones['idle'][self.__frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.__estado = 'idle'
        self.__mirar_derecha = True
        self.__is_grounded = False
        self.__en_techo = False
        self.__a_derecha = False
        self.__a_izquierda = False
        self.__get_hit = False
        
        #puntaje enemigo muerto
        self.__puntaje = self.__enemy_configs.get('puntaje_por_gole')

        #vida
        self.__vidas = self.__enemy_configs.get('vidas')
        self.is_alive = self.__enemy_configs.get('alive')

        #ataque
        self.__is_atacking = False
        self.__is_shooting = False
        self.__fuerza = self.__enemy_configs.get('fuerza')
        self.__proyectil_group = pg.sprite.Group()
        self.__tiempo_disparo = 0
        self.__disparo_cooldown = self.__enemy_configs.get('disparo_cooldown')
        self.__ready = True
        self.__fuerza_proyectil = self.__enemy_configs.get('fuerza_proyectil')
        self.__proyectil_size = self.__enemy_configs.get('proyectil_size')
        
        #movimiento
        self.__direccion = pg.math.Vector2(1,0)
        self.__speed =  self.__enemy_configs.get('speed')
        self.__gravedad = gravedad
        self.__distancia_recorrida = random.randint(15,32)
        self.__frame_movimiento = 0
        self.__is_idle = False
        self.__frame_idle = 0
        self.__campo_vision = pg.Rect(0,0,150,self.rect.height)


    @property
    def speed(self):
        return self.__speed
    
    @speed.setter
    def speed(self,velociadad):
        self.__speed = velociadad

    @property
    def direccion(self):
        return self.__direccion
    
    @direccion.setter
    def direccion(self,direccion):
        self.__direccion = direccion
    
    @property
    def frame_movimiento(self):
        return self.__frame_movimiento
    
    @frame_movimiento.setter
    def frame_movimiento(self,movimiento):
        self.__frame_movimiento = movimiento
    
    @property
    def fuerza(self):
        return self.__fuerza
    
    @fuerza.setter
    def fuerza(self,aumento_fuerza):
        self.__fuerza = aumento_fuerza
    
    @property
    def a_derecha(self):
        return self.__a_derecha
    
    @a_derecha.setter
    def a_derecha(self,derecha):
        self.__a_derecha = derecha

    @property
    def a_izquierda(self):
        return self.__a_izquierda
    
    @a_derecha.setter
    def a_izquierda(self,izquierda):
        self.__a_izquierda = izquierda
    
    @property
    def campo_vision(self):
        return self.__campo_vision
    
    @campo_vision.setter
    def campo_vision(self,vision):
        self.__campo_vision = vision

    @property
    def ready(self):
        return self.__ready
    
    @ready.setter
    def ready(self,ready_to_shoot):
        self.__ready = ready_to_shoot

    @property
    def tiempo_disparo(self):
        return self.__tiempo_disparo
    
    @tiempo_disparo.setter
    def tiempo_disparo(self,disparo):
        self.__tiempo_disparo = disparo
    
    @property
    def proyectil_group(self):
        return self.__proyectil_group
    
    @proyectil_group.setter
    def proyectil_group(self,proyectil):
        self.__proyectil_group = proyectil
        
    @property
    def fuerza_proyectil(self):
        return self.__fuerza_proyectil
    
    @property
    def puntaje(self):
        return self.__puntaje

    def importar_enemy_assest(self):
        self.__animaciones = importar_carpeta(self.__enemy_configs.get('path'),carpetas_bool = True)

        for animacion in self.__animaciones.keys():
            path_completo = self.__enemy_configs.get('path') + animacion
            self.__animaciones[animacion] = importar_carpeta(path_completo,imagenes_bool = True)

    def enemy_estado(self):
        lista_estados = [key for key in self.__animaciones]
        if self.__vidas > 0:
            self.is_alive = True
            if self.__is_shooting and 'shoot' in lista_estados:
                self.__estado = 'shoot'
            elif self.__get_hit and 'damage' in lista_estados:
                self.__estado = 'damage'
            else:
                self.__estado = 'idle'
        else:
            self.is_alive = False
            self.__estado = 'death'

    def tomar_direccion_imagen(self,image):
        if self.__mirar_derecha:
            self.image = image
        else:
            imagen_rotada = pg.transform.flip(image,True,False)
            self.image = imagen_rotada

    def play_animacion(self,delta_ms):
        animacion = self.__animaciones[self.__estado]

        self.__velocidad_animacion += delta_ms
        if self.__velocidad_animacion >= self.__frame_rate:
            self.__frame_index += 1
            self.__frame_index %= len(animacion)
            image = animacion[self.__frame_index]
            self.tomar_direccion_imagen(image)
            self.__velocidad_animacion = 0
            if self.__estado == 'shoot' and self.__frame_index >= (len(animacion) -1):
                self.__is_shooting = False
            if self.__estado == 'damage' and self.__frame_index >= (len(animacion) -1):
                self.__get_hit = False
            if self.__estado == 'death' and self.__frame_index >= (len(animacion) -1):
                self.kill()
        
        

        #Control de coliciones con los objetos del mapa
        # if self.__is_grounded and self.__a_derecha:
        #     self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        # elif self.__is_grounded and self.__a_izquierda:
        #     self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        # elif self.__is_grounded:
        #     self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # elif self.__en_techo and self.__a_derecha:
        #     self.rect = self.image.get_rect(topright = self.rect.topright)
        # elif self.__en_techo and self.__a_izquierda:
        #     self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # elif self.__en_techo:
        #     self.rect = self.image.get_rect(midtop = self.rect.midtop)
        
    def moviemiento_enemigo(self):
        if self.__vidas > 0 and self.__estado != 'death':
            if not self.__is_idle and random.randint(1,200) == 1:
                self.__direccion.x = 0
                self.__is_idle = True
                self.__frame_idle = 50
            if not self.__is_shooting :
                if not self.__is_idle:
                    if self.__direccion.x == 1:
                        self.__mirar_derecha = True
                    else:
                        self.__mirar_derecha = False
                        if self.__frame_movimiento > self.__distancia_recorrida:
                            self.__direccion.x *= -1
                            self.__frame_movimiento *= -1
                else:
                    self.__frame_idle -= 1
                    if self.__frame_idle <= 0:
                        self.__is_idle = False
                        self.__direccion.x = 1
    

    def get_grounded(self):
        self.__direccion.y += self.__gravedad
        self.rect.y += self.__direccion.y
    
    def atack(self):
        self.__is_atacking = True
        self.__frame_index = 0
    
    def shoot(self):
        self.__is_shooting = True
        self.__frame_index = 0
        self.__proyectil_group.add(self.crear_proyectil())

    def hit(self, golpe):
        self.__get_hit = True
        self.__is_shooting = False
        self.__direccion.x *= 1
        self.__vidas -= golpe
    
    def cooldown(self):
        if not self.__ready:
            curent_time = pg.time.get_ticks()
            if curent_time - self.__tiempo_disparo >= self.__disparo_cooldown:
                self.__is_shooting = False
                self.__ready = True
                self.__frame_index = 0
    

    def crear_proyectil(self):
        if self.__mirar_derecha:
            return Proyectil(self.rect.centerx, self.rect.centery, 'derecha',self.__enemy_configs.get('path'),True,self.__proyectil_size) 
        else:
            return Proyectil(self.rect.centerx, self.rect.centery, 'izquierda',self.__enemy_configs.get('path'), True,self.__proyectil_size) 

    def update(self,mover,delta_ms,pausa):
        if not pausa:
            self.rect.x += mover
            self.cooldown()
            self.moviemiento_enemigo()
            self.enemy_estado()
            self.play_animacion(delta_ms)


        
