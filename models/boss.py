import pygame as pg
from models.enemy import Enemy

class Boss(Enemy):
    def __init__(self, pos, gravedad, enemy_configs: dict):
        super().__init__(pos, gravedad, enemy_configs)
        self.importar_enemy_assest()
        self.campo_vision.width = 500
        self.damage_hitbox = pg.Rect(0,0,80,80)

    def golpe_expansivo(self):
        self.__is_hitting = True
        
        if self.__is_hitting:
            if self.__mirar_derecha:
                self.__onda_expansiva = pg.Rect(self.rect.centerx,self.rect.y, 30 + self.rect.width, self.rect.height - 5)
            else:
                self.__onda_expansiva = pg.Rect(self.rect.centerx - 45,self.rect.y, 20 + self.rect.width, self.rect.height)
    

    def update(self, mover, delta_ms, pausa):
        return super().update(mover, delta_ms, pausa)
        