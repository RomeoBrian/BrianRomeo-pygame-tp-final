import pygame as pg, sys
from settings.constantes import ANCHO,ALTO,FPS,open_configs
from settings.utils import crear_base_de_datos,insertar_en_base_de_datos,select_delete_en_base_de_datos,ultimo_id_insertado,update_en_base_de_datos
from models.botones import Boton
from models.ui import Ui

class Opciones():
    def __init__(self,click: bool,pantalla) -> None:
        self.__button_image = pg.image.load(open_configs().get('ui_settings').get('boton')).convert_alpha()
        self.__pantalla = pantalla
        #crear Boton
        self.__boton_audio = Boton(self.__pantalla,open_configs().get('ui_settings'),((ANCHO/2),(ALTO/2) - 90),'AUDIO',None,'white',0.5)
        self.__boton_teclas = Boton(self.__pantalla,open_configs().get('ui_settings'),((ANCHO/2),(ALTO/2) - 10),'TECLAS',None,'white',0.5)
        self.__boton_volver = Boton(self.__pantalla,open_configs().get('ui_settings'),((ANCHO/2),(ALTO/2) + 70),'VOLVER',None,'white',0.5)
        self.__boton_volver_score = Boton(self.__pantalla,open_configs().get('ui_settings'),((ANCHO - 150),(ALTO - 60)),'VOLVER',None,'white',0.5)
        self.__clicked = click
        self.__texto = ''
        self.__scores = ''
        #ui
        self.__ui = Ui(self.__pantalla,open_configs().get('ui_settings'))

        

    def menu_opciones(self,volver_estado,menu_anterior):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if evento.type == pg.MOUSEBUTTONUP:
                    self.__clicked = False
        
        self.__ui.dibujar_texto('Opciones',50,((ANCHO/2),(ALTO/2) - 300),'white')
        if self.__boton_audio.draw(self.__pantalla) and not self.__clicked:
            print('audio')
            self.__clicked = True
        if self.__boton_teclas.draw(self.__pantalla) and not self.__clicked:
            print('teclas')
            self.__clicked = True
        if self.__boton_volver.draw(self.__pantalla) and not self.__clicked:
            match menu_anterior:
                case 'nivel':
                    volver_estado('nivel')
                case 'main':
                    volver_estado('main')
            self.__clicked = True

    def pantalla_ingreso_nombre(self,manejar_estado):
        
        self.__ui.dibujar_texto('Ingrese su nombre',50,((ANCHO/2),(ALTO/2) - 300),'white')

        for evento in pg.event.get():
            if evento.type == pg.KEYDOWN:
                if evento.unicode.isalnum():
                    self.__texto += evento.unicode
                elif evento.key == pg.K_BACKSPACE:
                    self.__texto = self.__texto[:-1]
                elif evento.key == pg.K_RETURN:
                    #play(2,texto)
                    crear_base_de_datos('create table scores (id integer,nombre text,puntos_primer_nivel integer,puntos_segundo_nivel integer,puntos_tercer_nivel integer)')
                    sentencia = "insert into scores(id,nombre,puntos_primer_nivel,puntos_segundo_nivel,puntos_tercer_nivel) values(?,?,?,?,?)"
                    nombre = self.__texto
                    datos_bd = (f"0,{nombre},0,0,0")
                    datos = datos_bd.split(',')
                    insertar_en_base_de_datos(sentencia,[datos])
                    manejar_estado('game')
                    self.__texto = ""
            elif evento.type == pg.QUIT:
                return
        
        self.__ui.dibujar_texto(self.__texto,20,self.__pantalla.get_rect().center,'white')
    

    def mostar_higscore(self,volver_estado,menu_anterior):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if evento.type == pg.MOUSEBUTTONUP:
                    self.__clicked = False

        self.__ui.dibujar_texto('Higscore',50,((ANCHO/2),(ALTO/2) - 300),'white')

        
        self.__ui.dubijar_texto_doble_linea('NOMBRE | HIGSCORE',(((ANCHO/2) - 250),(ALTO/2) - 220),30,'white')
        higscores = select_delete_en_base_de_datos('SELECT id, nombre, puntos_primer_nivel+puntos_segundo_nivel+puntos_tercer_nivel AS suma','FROM scores ORDER BY suma Desc')
        nombres = ''
        score = ''
        for lista_higscore in higscores:
            if lista_higscore[0] != 0:
                nombres += f'{lista_higscore[1][0:5]}\n'
                score += f'{lista_higscore[2]}\n'
        
        self.__ui.dubijar_texto_doble_linea(nombres,(((ANCHO/2) - 230),(ALTO/2) - 185),30,'white')
        self.__ui.dubijar_texto_doble_linea(score,(((ANCHO/2)+ 50),(ALTO/2) - 185),30,'white')

        if self.__boton_volver_score.draw(self.__pantalla) and not self.__clicked:
            match menu_anterior:
                case 'seleccion':
                    volver_estado('seleccion')
            self.__clicked = True