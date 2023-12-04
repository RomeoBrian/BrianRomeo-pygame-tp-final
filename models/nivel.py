import pygame as pg, random
from settings.constantes import TILEZISE,ANCHO,ALTO,open_configs
from settings.utils import tileBackground,select_delete_en_base_de_datos,ultimo_id_insertado,update_en_base_de_datos
from models.tiles import Tile
from models.boundries import Boundry
from models.player import Player
from models.enemy import Enemy
from models.trampas import Trampa
from models.items import Items
from models.ui import Ui
from models.botones import Boton
from models.hints import Hint
from models.boss import Boss


class Nivel:
    def __init__(self,surface,diccionario_nivel: dict,crear_seleccion_nivel,nivel_actual) -> None:
        self.__pantalla = surface
        self.__trasparent_surface = pg.Surface((ANCHO,ALTO), pg.SRCALPHA)
        self.__nivel_config = diccionario_nivel
        self.__nivel_actual = nivel_actual
        self.__tile_settings = open_configs().get('map_settings')
        self.__select_id_usuario = select_delete_en_base_de_datos('SELECT oid FROM','scores ORDER BY oid desc')
        self.__id_usuario = self.__select_id_usuario[0][0]
        #ui
        self.__ui = Ui(self.__pantalla,open_configs().get('ui_settings'))
        self.crear_nivel(self.__nivel_config.get('MAP'))
        self.__alive = True
        self.__lugar_player = 0
        self.__lugar_enemy = 0
        self.__movimiento_camara = pg.math.Vector2()
        self.__enemy_collision = False
        self.__sobrecitos_coin_recolectados = 0
        self.crear_seleccion_nivel = crear_seleccion_nivel
        self.__cliked = False
        self.__boton_siguiente_nivel = Boton(self.__pantalla,open_configs().get('ui_settings'),((ANCHO/2) - 100,(ALTO/2) - 90),'SIGUIENTE NIVEL',None,'white',0.5)
        self.__boton_reintentar = Boton(self.__pantalla,open_configs().get('ui_settings'),((ANCHO/2),(ALTO/2) - 90),'REINTENTAR',None,'white',0.5)
        if self.__nivel_actual == 0:
            self.__doble_salto = False
        else:
            self.__doble_salto = True

        #puntaje
        self.__puntaje = 0
        
        #background
        self.__fondo_stone = pg.image.load('./assets/graphics/background/background_stone.png').convert_alpha()
        self.__fondo_stone = pg.transform.scale(self.__fondo_stone,(self.__fondo_stone.get_width()*2,self.__fondo_stone.get_height()*2))

        #musica
        # pg.mixer.music.load(self.__nivel_config.get('main_theme'))
        # pg.mixer.music.play(loops= -1)
        # pg.mixer.music.set_volume(0.4)
        #volver a poner en casa
        self.__main_theme = pg.mixer.Sound(self.__nivel_config.get('main_theme'))
        self.__main_theme.play(loops=-1)
        self.__main_theme.set_volume(0.4)
     
    @property
    def sobrecito_coin(self):
        return self.__sobrecitos_coin_recolectados
    
    @property
    def player(self):
        return self.__player

    @property
    def nivel_actual(self):
        return self.__nivel_actual

    @property
    def main_theme(self):
        return self.__main_theme

    def crear_nivel(self,layout):
        self.__tiles = pg.sprite.Group()
        self.__boundry = pg.sprite.Group()
        self.__player = pg.sprite.GroupSingle()
        self.__enemy = pg.sprite.Group()
        self.__trampa = pg.sprite.Group()
        self.__sobrecitos = pg.sprite.Group()
        self.__fish_salto = pg.sprite.GroupSingle()
        self.__mensaje = pg.sprite.Group()
        self.__jefe_final = pg.sprite.GroupSingle()
        for filas_index,filas in enumerate(layout):
            for col_index,celda in enumerate(filas):
                x = col_index * TILEZISE
                y = filas_index * TILEZISE
                for key,tiles in self.__tile_settings.items():
                    match key:
                        case 'tiles_movimiento':
                            for key, valor in tiles.items():
                                if celda == key:
                                    tile = Tile((x,y),TILEZISE,[valor],is_movable = True, direccion_y = True)
                                    self.__tiles.add(tile)
                        case 'tiles_invisibles':
                            for key, valor in tiles.items():
                                if celda == key:
                                    if key == 'b':
                                        boundries = Boundry((x,y),TILEZISE)
                                        self.__boundry.add(boundries)
                                    elif key == '!':
                                        mensaje = Hint((x,y),TILEZISE,self.__pantalla,"Busca\nArriba")
                                        self.__mensaje.add(mensaje)
                                    else:
                                        boundries = Boundry((x,y),TILEZISE,valor)
                                        self.__boundry.add(boundries)
                        case "entidades":
                            for key, valor in tiles.items():
                                if celda == key:
                                    if key == 'P':
                                        player_sprite = Player((x,y),self.__nivel_config.get('gravedad'),self.__nivel_config.get(valor),self.__pantalla)
                                        self.__player.add(player_sprite)
                                    elif key == 'E':
                                        enemy_sprite = Enemy((x,y),self.__nivel_config.get('gravedad'),self.__nivel_config.get('enemy').get(random.choices(valor,self.__nivel_config.get('enemy_weights'))[0]))
                                        self.__enemy.add(enemy_sprite)
                                    elif key == 'T':
                                        trampa = Trampa((x,y),TILEZISE,[valor])
                                        self.__trampa.add(trampa)
                                    elif key == 'f':
                                        sobrecitos = Items((x,y),TILEZISE,self.__nivel_config.get(valor),None,self.__pantalla)
                                        self.__sobrecitos.add(sobrecitos)
                                    elif key == 'S' and self.__nivel_actual == 0:
                                        fish_salto = Items((x,y),TILEZISE,self.__nivel_config.get(valor),'DOBLE\nSALTO',self.__pantalla)
                                        self.__fish_salto.add(fish_salto)
                                    elif key == 'B' and self.__nivel_actual == 2:
                                        jefe = Boss((x,y),self.__nivel_config.get('gravedad'),self.__nivel_config.get(valor))
                                        self.__enemy.add(jefe)
                        case _:
                            for key, valor in tiles.items():
                                if celda == key:
                                    tile = Tile((x,y),TILEZISE,[valor])
                                    self.__tiles.add(tile)
    
    


    def movimiento_horizontal_colisiones(self,delta_ms):
        player = self.__player.sprite
        player.rect.x += player.direccion.x * player.speed
        enemys = self.__enemy.sprites()
        #colision del player con el entorno
        for tile_sprite in self.__tiles.sprites():
            if tile_sprite.rect.colliderect(player.rect):
                if player.direccion.x < 0 and not tile_sprite.is_movable:
                    player.frame_index = 0
                    player.rect.left = tile_sprite.rect.right + 3
                    player.a_izquierda = True
                    self.__lugar_player = player.rect.left
                elif player.direccion.x > 0 and not tile_sprite.is_movable:
                    player.frame_index = 0
                    player.rect.right = tile_sprite.rect.left  - 3
                    player.a_derecha = True
                    self.__lugar_player = player.rect.right
        
        for enemigo in enemys:
            enemigo.rect.x += enemigo.direccion.x * enemigo.speed
            enemigo.frame_movimiento += 1
            if self.__nivel_actual == 2:
                enemigo.damage_hitbox.center = (enemigo.rect.centerx,enemigo.rect.centery - 80)
                #pg.draw.rect(self.__pantalla,'white',enemigo.damage_hitbox)
            if enemigo.direccion.x != 0:
                enemigo.campo_vision.center = (enemigo.rect.centerx + (75 * enemigo.direccion.x),enemigo.rect.centery)
                #pg.draw.rect(self.__pantalla,'white',enemigo.campo_vision)
            if enemigo.campo_vision.colliderect(player.rect) and enemigo.ready and enemigo.is_alive:
                enemigo.shoot()
                enemigo.ready = False
                enemigo.tiempo_disparo = pg.time.get_ticks()
                
            for boundry_sprite in self.__boundry.sprites():
                if boundry_sprite.rect.colliderect(enemigo.rect):
                    if enemigo.direccion.x < 0:
                        enemigo.direccion.x = 1
                        enemigo.rect.left = boundry_sprite.rect.right + 3
                        enemigo.a_izquierda = True
                        self.__lugar_enemy = enemigo.rect.left
                    elif enemigo.direccion.x > 0:
                        enemigo.rect.right = boundry_sprite.rect.left - 3
                        enemigo.direccion.x = -1
                        enemigo.a_derecha = True
                        self.__lugar_enemy = enemigo.rect.right
                        
            for tile_sprite in self.__tiles.sprites():
                if tile_sprite.rect.colliderect(enemigo.rect):
                    if enemigo.direccion.x < 0 and not tile_sprite.is_movable:
                        enemigo.frame_index = 0
                        enemigo.rect.left = tile_sprite.rect.right + 3
                        enemigo.direccion.x = 1
                        enemigo.a_izquierda = True
                        self.__lugar_enemy = enemigo.rect.left
                    elif enemigo.direccion.x > 0 and not tile_sprite.is_movable:
                        enemigo.frame_index = 0
                        enemigo.rect.right = tile_sprite.rect.left - 3
                        enemigo.direccion.x = -1
                        enemigo.a_derecha = True
                        self.__lugar_enemy = enemigo.rect.right
            
        #enemy
        if len(self.__enemy) > 0:
            if enemigo.a_izquierda and (enemigo.rect.left < self.__lugar_enemy or enemigo.direccion.x >= 0):
                enemigo.a_izquierda = False
            if enemigo.a_derecha and (enemigo.rect.right > self.__lugar_enemy or enemigo.direccion.x <= 0):
                enemigo.a_derecha = False
                    
        #player
        if player.a_izquierda and (player.rect.left < self.__lugar_player or player.direccion.x >= 0):
            player.a_izquierda = False
        if player.a_derecha and (player.rect.right > self.__lugar_player or player.direccion.x <= 0):
            player.a_derecha = False

        

    
    def movimiento_vertical_colisiones(self,delta_ms):
        player = self.__player.sprite
        player.get_grounded()
        enemys = self.__enemy.sprites()
        for tile_sprite in self.__tiles.sprites():
            if tile_sprite.rect.colliderect(player.rect):
                if player.direccion.y > 0:
                    player.rect.bottom = tile_sprite.rect.top
                    player.direccion.y = 0
                    player.is_grounded = True
                    player.jump_count = 2
                    player.do_salto = True
                    player.do_doble_salto = self.__doble_salto                   
                elif player.direccion.y < 0:
                    player.rect.top = tile_sprite.rect.bottom
                    player.direccion.y = 0
                    player.en_techo = True
                    
        for enemigo in enemys:
            enemigo.get_grounded()
            for tile_sprite in self.__tiles.sprites():
                if tile_sprite.rect.colliderect(enemigo.rect):
                    if enemigo.direccion.y > 0:
                        enemigo.rect.bottom = tile_sprite.rect.top
                        enemigo.direccion.y = 0
                        enemigo.is_grounded = True                  
                    elif enemigo.direccion.y < 0:
                        enemigo.rect.top = tile_sprite.rect.bottom
                        enemigo.direccion.y = 0
                        enemigo.en_techo = True
                
    
        if player.is_grounded and player.direccion.y < 0 or player.direccion.y > 1:
            player.is_grounded = False
        if player.en_techo and player.direccion.y > 0:
            player.en_techo = False
    
    def mover_camara(self,pausa):
        player = self.__player.sprite
        player_x = player.rect.centerx
        player_y = player.rect.centery
        direccion_x = player.direccion.x
        if not pausa:
            if player_x < self.__pantalla.get_width()/4 and direccion_x < 0:
                self.__movimiento_camara[0] = self.__nivel_config.get('velocidad_mover_mapa')
                player.speed = 0
            elif player_x > self.__pantalla.get_width() - (self.__pantalla.get_width()/4) and direccion_x > 0:
                self.__movimiento_camara[0] = -self.__nivel_config.get('velocidad_mover_mapa')
                player.speed = 0
            else:
                self.__movimiento_camara[0] = 0
                player.speed = self.__nivel_config.get('player').get('speed')
        else:
            self.__movimiento_camara[0] = 0
            player.speed = self.__nivel_config.get('player').get('speed')

    def ataque_enemigo(self):
        for enemigos in self.__enemy:
            if pg.sprite.spritecollide(enemigos, self.__player, False):
                self.__enemy_collision = True

    def damage_trampas(self):
        for trampas in self.__trampa:
            #pg.draw.rect(self.__pantalla,'red',trampas.rect)
            if trampas.rect.colliderect(self.__player.sprite.rect):
                trampas.contacto = True                

    def pantalla_win_loose(self,mensaje,color):
        color_fondo_gana = (20, 19, 39,150)
        pg.draw.rect(self.__trasparent_surface,color_fondo_gana,[0,0,ANCHO,ALTO])
        self.__pantalla.blit(self.__trasparent_surface,(0,0))
        self.__ui.dibujar_texto(mensaje,50,((ANCHO/2),(ALTO/2) - 300),color)

    def run(self,delta_ms,pausa,touch_space,minutos):        
        self.mover_camara(pausa)
        
        #background
        tileBackground(self.__fondo_stone,self.__pantalla)

        #mensaje
        self.__ui.dibujar_texto('Para moverte podes usar awsd',50,(50,50),'white')

        #tiles
        self.__tiles.update(self.__movimiento_camara[0])
        self.__tiles.draw(self.__pantalla)
        # for tiles in self.__tiles:
        #     pg.draw.rect(self.__pantalla,'red',tiles.rect)

        #boundries
        self.__boundry.update(self.__movimiento_camara[0])
        self.__boundry.draw(self.__pantalla)
        #for boundries in self.__boundry:
        #    self.__pantalla.blit(boundries.image,(0,0))

        #Hint
        self.__mensaje.update(self.__movimiento_camara[0])
        self.__mensaje.draw(self.__pantalla)

        #player
        self.__player.update(delta_ms,pausa,touch_space)
        if not pausa and self.__alive:
            self.movimiento_horizontal_colisiones(delta_ms)
            self.movimiento_vertical_colisiones(delta_ms)
        self.__player.draw(self.__pantalla)
        #pg.draw.rect(self.__pantalla,'red',self.__player.sprite.rect)
        #pg.draw.circle(self.__pantalla, 'red',(self.__player.sprite.rect.centerx+10,self.__player.sprite.rect.centery) ,self.__player.sprite.radius)

        #enemy
        self.__enemy.update(self.__movimiento_camara[0],delta_ms,pausa)
        self.__enemy.draw(self.__pantalla)
        
        #trampa
        self.__trampa.update(self.__movimiento_camara[0])
        self.__trampa.draw(self.__pantalla)

        #sobrecito
        self.__sobrecitos.update(self.__movimiento_camara[0],delta_ms,pausa)
        self.__sobrecitos.draw(self.__pantalla)

        #fish_salto
        if self.__nivel_actual == 0:
            self.__fish_salto.update(self.__movimiento_camara[0],delta_ms,pausa)
            self.__fish_salto.draw(self.__pantalla)
        
        #proyectil
        self.__player.sprite.proyectil_group.update(delta_ms)
        # for proyectil in self.__player.sprite.proyectil_group:
        #     pg.draw.rect(self.__pantalla,'red',proyectil.rect)
        self.__player.sprite.proyectil_group.draw(self.__pantalla)

        for enemigo in self.__enemy:
            enemigo.proyectil_group.update(delta_ms)
            enemigo.proyectil_group.draw(self.__pantalla)
        
        
        #colliosiones y muertes del enemigo
        if self.__player.sprite.is_hitting:
            for enemigos in self.__enemy:
                if self.__player.sprite.atack_rect.colliderect(enemigos):
                    self.__puntaje += enemigos.puntaje
                    enemigos.hit(self.__player.sprite.fuerza)
                    self.__player.sprite.is_hitting = False
            
            #colision bala del player con enemigo    
            if self.__nivel_actual == 2:
                for enemigos in self.__enemy:
                    for player_proyectil in self.__player.sprite.proyectil_group.sprites():
                        if enemigos.damage_hitbox.colliderect(player_proyectil.rect):
                            enemigo.hit(self.__player.sprite.fuerza_disparo)
                            player_proyectil.kill()
                            self.__player.sprite.is_hitting = False
            else:
                enemigo_golpeado = pg.sprite.groupcollide(self.__player.sprite.proyectil_group,self.__enemy,True,False)
                for key in enemigo_golpeado:
                    self.__puntaje += enemigo_golpeado[key][0].puntaje
                    enemigo_golpeado[key][0].hit(self.__player.sprite.fuerza_disparo)
                    self.__player.sprite.is_hitting = False
            

        #colision proyectil con tiles
        pg.sprite.groupcollide(self.__player.sprite.proyectil_group,self.__tiles,True,False)
        for enemigos in self.__enemy:
            pg.sprite.groupcollide(enemigos.proyectil_group,self.__tiles,True,False)

        #player death
        self.ataque_enemigo()
        if self.__enemy_collision:
            self.__enemy_collision = False
            self.__player.sprite.recibir_golpe(1)  
        
        #contacto con trampa
        self.damage_trampas()
        for trampa in self.__trampa:
            if trampa.contacto == True:
                damage = trampa.do_damage()
                self.__player.sprite.recibir_golpe(damage)

        #colision con sobrecito
        sobrecito_obteniodo = pg.sprite.groupcollide(self.__player,self.__sobrecitos,False,True)
        #if pg.sprite.spritecollide(self.__player.sprite, self.__sobrecitos,True):
        for sobrecito in sobrecito_obteniodo:
            self.__puntaje += 100
            self.__player.sprite.heal(sobrecito_obteniodo[sobrecito][0].regenera_vida)
            self.__sobrecitos_coin_recolectados += 1
            if len(self.__sobrecitos) == 0:
                print('Se recolectaron todos los fish coin')

        #colision con fish_Salto
        if pg.sprite.spritecollide(self.__player.sprite, self.__fish_salto,True):
            self.__doble_salto = True
        
        #golpe del proyectil al enemigo
        for enemigo in self.__enemy:
            if pg.sprite.spritecollide(self.__player.sprite,enemigo.proyectil_group, True):
                self.__player.sprite.recibir_golpe(enemigo.fuerza_proyectil)

        #condicion de Victoria
        if self.__player.sprite.vidas > 0:
            if len(self.__sobrecitos) == 0 and len(self.__enemy) == 0:
                if self.__nivel_actual == 0:
                    update_en_base_de_datos(f'set puntos_primer_nivel = {self.__puntaje}, id = {self.__id_usuario}','scores',f'oid = {self.__id_usuario}')
                elif self.__nivel_actual == 1:
                    update_en_base_de_datos(f'set puntos_segundo_nivel = {self.__puntaje}','scores',f'oid = {self.__id_usuario}')
                elif self.__nivel_actual == 2:
                    update_en_base_de_datos(f'set puntos_tercer_nivel = {self.__puntaje}','scores',f'oid = {self.__id_usuario}')

                self.pantalla_win_loose('GANASTE!!!!','white')
                if self.__boton_siguiente_nivel.draw(self.__pantalla) and not self.__cliked:
                        self.crear_seleccion_nivel(self.__nivel_actual,self.__nivel_config['desbloquea'])            
                        self.__cliked = True
        else:
            self.__alive == False
            self.pantalla_win_loose('PERDISTE!!!!','white')
            if self.__boton_reintentar.draw(self.__pantalla) and not self.__cliked:
                    self.crear_seleccion_nivel(self.__nivel_actual,self.__nivel_actual)
                    self.__cliked = True
        

