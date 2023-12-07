from os import walk
import pygame as pg
import re, sqlite3


def importar_carpeta(path,carpetas_bool = False, imagenes_bool = False):
    dict_animaciones = {}
    lista_imagenes = []
    for _,carpetas,imagenes in walk(path):
        if carpetas_bool:
            for indice_carpetas in range(len(carpetas)):
                dict_animaciones[carpetas[indice_carpetas]] = [] 
        if imagenes_bool:
            for imagen in imagenes:
                path_con_imagen = path + '/' + imagen
                imagen_surf = pg.image.load(path_con_imagen).convert_alpha()
                if re.findall("player", path):
                    ancho = imagen_surf.get_width()
                    alto = imagen_surf.get_height()
                    imagen_surf = pg.transform.scale(imagen_surf,(ancho*3,alto*3))
                if re.findall("summon", path):
                    ancho = imagen_surf.get_width()
                    alto = imagen_surf.get_height()
                    imagen_surf = pg.transform.scale(imagen_surf,(ancho*3,alto*3))
                if re.findall("mecha-boss", path):
                    ancho = imagen_surf.get_width()
                    alto = imagen_surf.get_height()
                    imagen_surf = pg.transform.scale(imagen_surf,(ancho*6,alto*6))
                lista_imagenes.append(imagen_surf)
    
    if carpetas_bool:
        return dict_animaciones
    if imagenes_bool:
        return lista_imagenes

def tileBackground(image: pg.Surface,pantalla) -> None:
        screenWidth, screenHeight = pantalla.get_size()
        imageWidth, imageHeight = image.get_size()
        
        # Calculate how many tiles we need to draw in x axis and y axis
        tilesX = int(screenWidth / imageWidth) + 1
        tilesY = int(screenHeight / imageHeight) + 1
        # Loop over both and blit accordingly
        for x in range(tilesX):
            for y in range(tilesY):
                pantalla.blit(image, (x * imageWidth, y * imageHeight))


def crear_base_de_datos(sentencia: str):
        '''
        Creamos la conexion con la base de dato y la tabla para trabajar
        Recibe: nada
        Devuelve: nada
        '''
        with sqlite3.connect(f"./database/scores.db") as conexion:
            try:
                crear_tabla = sentencia
                conexion.execute(crear_tabla)
                print("se creo la tabla")                        
            except sqlite3.OperationalError:
                print("La tabla ya existe")

def insertar_en_base_de_datos(sentencia: str,valores: list):
    '''
    Generamos la QRY para insertar datos en la tabla
    Recibe: la sentencia insert y los valores a insertar
    Devuelve: nada
    '''
    with sqlite3.connect(f"./database/scores.db") as conexion:
        try:
            conexion.executemany(sentencia,valores)
            conexion.commit()
            print('Se insertaron los datos Correctamente!')
        except:
            print('Se produjo un error al insertar los datos')

def ultimo_id_insertado():
    '''
    Tomamos el ultimo id insertado en la tabla
    Recibe: nada
    Devuelve: el id
    '''
    with sqlite3.connect(f"./database/scores.db") as conexion:
        try:
            ultimo_id = f'SELECT last_insert_rowid();'
            cursor  = conexion.execute(ultimo_id)
            conexion.commit()
            rows = cursor.fetchall()
            return rows
        except:
            print('Se produjo un error al insertar los datos')

def select_delete_en_base_de_datos(statement: str,tabla: str,condicion = '1=1'):
    '''
    Generamos la QRY para hacer un delete en la tabla
    Recibe: el statement, la tabla en cueston y la condicion si se desea eliminar un dato especifico
        sino queda 1=1 para pasar el where
    Devuelve: nada
    '''
    print(statement,tabla)
    with sqlite3.connect(f"./database/scores.db") as conexion:
        try:
            sentencia = f'{statement} {tabla}'
            cursor  = conexion.execute(sentencia)
            conexion.commit()
            rows = cursor.fetchall()
            return rows
        except:
            print('Se produjo un error al seleccionar/deletear los datos')

def update_en_base_de_datos(statement: str,tabla: str,condicion = '1=1'):
    '''
    Generamos la QRY para hacer un delete en la tabla
    Recibe: el statement, la tabla en cueston y la condicion si se desea eliminar un dato especifico
        sino queda 1=1 para pasar el where
    Devuelve: nada
    '''
    with sqlite3.connect(f"./database/scores.db") as conexion:
        try:
            sentencia = f'UPDATE {tabla} {statement} where {condicion}'
            cursor  = conexion.execute(sentencia)
            conexion.commit()
            rows = cursor.fetchall()
            return rows
        except:
            print('Se produjo un error al insertar los datos')