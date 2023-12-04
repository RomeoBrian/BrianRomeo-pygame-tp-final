import pygame as pg
from settings.constantes import ANCHO,FPS
from settings.utils import importar_carpeta
from models.proyectil import Proyectil


class Player(pg.sprite.Sprite):
    def __init__(self,pos,gravedad,diccionario_config: dict,pantalla):
        super().__init__()
        self.__player_config = diccionario_config
        self.importar_player_assest()
        self.__pantalla = pantalla
        #animacion
        self.__frame_rate = self.__player_config.get('frame_rate')
        self.__frame_index = 0
        self.__velocidad_animacion = self.__player_config.get('velocidad_animacion')
        self.image = self.__animaciones['idle'][self.__frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.__estado = 'idle'
        self.__mirar_derecha = True
        self.__is_grounded = False
        self.__en_techo = False
        self.__a_derecha = False
        self.__a_izquierda = False
        self.__ready = True
        self.__damage = False
        self.radius = 20
        self.__atack_rect = pg.Rect(0,0,0,0)

        #vida
        self.__vidas = self.__player_config.get('vida')
        self.__vida_maxima = self.__player_config.get('vida_maxima')
        self.__alive = True

        #ataque
        self.__is_atacking = False
        self.__is_hitting = False
        self.__is_shooting = False
        self.__fuerza = self.__player_config.get('fuerza')
        self.__fuerza_disparo = self.__player_config.get('fuerza_disparo')
        self.__proyectil_group = pg.sprite.Group()
        self.__tiempo_disparo = 0
        self.__disparo_cooldown = self.__player_config.get('disparo_cooldown')
        
        #movimiento
        self.__direccion = pg.math.Vector2(0,0)
        self.__speed = self.__player_config.get('speed')
        self.__gravedad = gravedad
        self.__altura_salto = self.__player_config.get('altura_salto')
        self.__do_salto = True
        self.__altura_salto += self.__altura_salto
        self.__velocidad_salto = self.__altura_salto/2
        print(self.__velocidad_salto)
        self.__jump_count = 2
        self.__do_doble_salto = self.__player_config.get('do_doble_salto')

        #sonidos
        self.__jump_sound = pg.mixer.Sound(self.__player_config.get('jump_sound'))
        self.__shoot_sound = pg.mixer.Sound(self.__player_config.get('shoot_sound'))

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
    def is_grounded(self):
        return self.__is_grounded

    @is_grounded.setter
    def is_grounded(self,grounded: bool):
        self.__is_grounded = grounded
    
    @property
    def en_techo(self):
        return self.__en_techo

    @en_techo.setter
    def en_techo(self,techo: bool):
        self.__en_techo = techo
    
    @property
    def a_derecha(self):
        return self.__a_derecha

    @a_derecha.setter
    def a_derecha(self,derecha: bool):
        self.__a_derecha = derecha
    
    @property
    def a_izquierda(self):
        return self.__a_izquierda

    @a_izquierda.setter
    def a_izquierda(self,izquierda: bool):
        self.__a_izquierda = izquierda
    
    @property
    def do_salto(self):
        return self.__do_salto

    @do_salto.setter
    def do_salto(self,saltar: bool):
        self.__do_salto = saltar
    
    @property
    def do_doble_salto(self):
        return self.__do_doble_salto

    @do_doble_salto.setter
    def do_doble_salto(self,saltar: bool):
        self.__do_doble_salto = saltar
    
    @property
    def do_super_salto(self):
        return self.__do_super_salto

    @do_super_salto.setter
    def do_super_salto(self,super_salto: bool):
        self.__do_super_salto = super_salto

    @property
    def proyectil_group(self):
        return self.__proyectil_group

    @proyectil_group.setter
    def proyectil_group(self,proyectil: bool):
        self.__proyectil_group = proyectil
    
    @property
    def frame_index(self):
        return self.__frame_index
    
    @frame_index.setter
    def frame_index(self,frame):
        self.__frame_index = frame

    @property
    def vidas(self):
        return self.__vidas
    
    @property
    def vida_maxima(self):
        return self.__vida_maxima

    @property
    def atack_rect(self):
        return self.__atack_rect

    @property
    def is_atacking(self):
        return self.__is_atacking

    @is_atacking.setter
    def is_atacking(self,atacking):
        self.__is_atacking = atacking
    
    @property
    def is_hitting(self):
        return self.__is_hitting

    @is_hitting.setter
    def is_hitting(self,hitting):
        self.__is_hitting = hitting
    
    @property
    def fuerza(self):
        return self.__fuerza

    @fuerza.setter
    def fuerza(self,aumento_fuerza):
        self.__fuerza = aumento_fuerza

    @property
    def fuerza_disparo(self):
        return self.__fuerza_disparo

    @fuerza_disparo.setter
    def fuerza_disparo(self,aumento_fuerza_disparo):
        self.__fuerza_disparo = aumento_fuerza_disparo
    
    @property
    def jump_count(self):
        return self.__jump_count

    @jump_count.setter
    def jump_count(self,jump_count):
        self.__jump_count = jump_count

    def importar_player_assest(self):
        path = self.__player_config.get('path')
        self.__animaciones = importar_carpeta(path,carpetas_bool= True) #{'idle': [], 'caer': [], 'correr': [], 'saltar': [], 'atack': [], 'shoot': []}
        
        for animacion in self.__animaciones.keys():
            path_completo = path + animacion
            self.__animaciones[animacion] = importar_carpeta(path_completo,imagenes_bool= True)

    def player_estado(self):
        if self.__vidas > 0:
            if self.__is_atacking:
                self.__estado = 'atack'
            elif self.__is_shooting:
                self.__estado = 'shoot'
            elif self.__direccion.y < 0 and not self.__is_grounded:
                self.__estado = 'saltar'
            elif self.__direccion.y > 0 and not self.__is_grounded:
                self.__estado = 'caer'
            elif self.__damage:
                self.__estado = 'damage'
            elif self.__direccion.x != 0:
                self.__estado = 'correr'
            else:
                if self.__is_grounded:
                    self.__estado = 'idle'
        else:
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
        if self.__is_shooting:
            self.__frame_rate = 80 
        if self.__velocidad_animacion >= self.__frame_rate:
            self.__frame_index += 1
            self.__frame_index %= len(animacion)
            image = animacion[self.__frame_index]
            self.tomar_direccion_imagen(image)
            self.__velocidad_animacion = 0
            if self.__estado == 'atack' and self.__frame_index == (len(animacion) -1):
                self.__is_atacking = False
            if self.__estado == 'shoot' and self.__frame_index == (len(animacion) -1):
                self.__is_shooting = False
            if self.__estado == 'damage' and self.__frame_index == (len(animacion) -1):
                self.__damage = False
            if self.__estado == 'death' and self.__frame_index == (len(animacion) -1):
                self.__alive = False
                print('murio')
        
        #Control de coliciones con los objetos del mapa
        if self.__is_grounded and self.__a_derecha:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.__is_grounded and self.__a_izquierda:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.__is_grounded:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.__en_techo and self.__a_derecha:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.__en_techo and self.__a_izquierda:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.__en_techo:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        

    def walk(self,derecha = True):
        if derecha:
            self.__direccion.x = 1
        else:
            self.__direccion.x = -1
        return self.__direccion.x
    

    def get_teclas(self,touch_space):
        teclas = pg.key.get_pressed()
        if teclas[pg.K_d] and not teclas[pg.K_a]:
            self.walk(True)
            self.__mirar_derecha = True     
        if teclas[pg.K_a] and not teclas[pg.K_d]:
            self.walk(False)
            self.__mirar_derecha = False
        if not teclas[pg.K_a] and not teclas[pg.K_d]:
            self.__direccion.x = 0
            self.__estado = 'idle'
        if touch_space and (self.__is_grounded or self.__jump_count >0):
            #if teclas[pg.K_SPACE] == 1 and (self.__is_grounded or self.__jump_count >0):    
            self.salto()       
        if teclas[pg.K_f] and not self.__is_atacking and self.__ready:
            self.atack()
            self.__ready = False
            self.__tiempo_disparo = pg.time.get_ticks()
        if teclas[pg.K_e] and not self.__is_shooting and self.__ready:
            self.shoot()
            self.__ready = False
            self.__tiempo_disparo = pg.time.get_ticks()
            


    def cooldown(self):
        if not self.__ready:
            curent_time = pg.time.get_ticks()
            if curent_time - self.__tiempo_disparo >= self.__disparo_cooldown:
                self.__is_shooting = False
                self.__ready = True
                self.__frame_index = 0

    def get_grounded(self):
        self.__direccion.y += self.__gravedad
        self.rect.y += self.__direccion.y
        self.__velocidad_salto = self.__altura_salto/2
        
        

    def salto(self):
            if self.__do_salto:
                self.__jump_sound.play()
                self.__jump_sound.set_volume(0.3)
                self.__direccion.y -= self.__velocidad_salto
                self.__velocidad_salto -= self.__gravedad
                self.__jump_count -= 1
                self.__do_salto = False
            elif self.__do_doble_salto and self.__direccion.y < 0:
                self.__jump_sound.play()
                self.__jump_sound.set_volume(0.3)
                self.__direccion.y -= self.__velocidad_salto
                self.__velocidad_salto -= self.__gravedad
                self.__jump_count -= 1
                self.__do_doble_salto = False
            elif self.__direccion.y < -self.__altura_salto and self.__jump_count == 0:
                    self.__velocidad_salto = self.__altura_salto/2
                    self.__jump_count = 2
                  
    
    def atack(self):
        self.__is_hitting = True
        self.__is_atacking = True
        self.__frame_index = 0
        if self.__is_hitting:
            if self.__mirar_derecha:
                self.__atack_rect = pg.Rect(self.rect.centerx,self.rect.y, 30 + self.rect.width, self.rect.height - 5)
            else:
                self.__atack_rect = pg.Rect(self.rect.centerx - 45,self.rect.y, 20 + self.rect.width, self.rect.height)
        #dibujo el rectangulo para probar como funciona.
        #pg.draw.rect(self.__pantalla, 'red',self.__atack_rect)
        
    
    def shoot(self):
        #self.__shoot_sound.play()
        #self.__shoot_sound.set_volume(0.1)
        self.__frame_index = 0
        self.__is_shooting = True
        self.__is_hitting = True
        self.__proyectil_group.add(self.crear_proyectil())
    
    def crear_proyectil(self):
        if self.__mirar_derecha:
            return Proyectil(self.rect.centerx, self.rect.centery, 'derecha',self.__player_config.get('path'),True) 
        else:
            return Proyectil(self.rect.centerx, self.rect.centery, 'izquierda',self.__player_config.get('path'), True)
    
    def recibir_golpe(self,golpe = 0):
        self.__vidas -= golpe
        self.__damage = True
    
    def heal(self,cantidad):
        if self.__vidas < self.__vida_maxima:
            self.__vidas += cantidad

        

    def update(self,delta_ms,pausa,touch_space):
        if not pausa and self.__alive:
            self.get_teclas(touch_space)
            self.cooldown()
            self.player_estado()
            self.play_animacion(delta_ms)


        
