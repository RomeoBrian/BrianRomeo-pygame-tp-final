import json

FPS = 60

ANCHO = 1200
ALTO = int(ANCHO * 0.7)
TILEZISE = 40
CONFIG_FILE_PATH = './configs/config.json'

def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)

