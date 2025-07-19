import csv
from pygame import Rect
from pgzero.actor import Actor
from config import *

TILE_SIZE = 16
TILESET_COLUMNS = 32

tileset_image = "dungeon_tile_set.png"


def load_csv(filename):
    try:
        with open(filename, newline="") as csvfile:
            reader = csv.reader(csvfile)
            return [[int(cell) for cell in row] for row in reader]
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {filename}")
        return []


class Tile:
    def __init__(self, tile_id, x, y):
        self.tile_id = tile_id
        self.x = x
        self.y = y

    def draw(self, offset_x=0, offset_y=0):
        if self.tile_id < 0:
            return
        col = self.tile_id % TILESET_COLUMNS
        row = self.tile_id // TILESET_COLUMNS
        tile_actor = Actor(tileset_image)
        
        # Aplicar offset para centralização
        tile_actor.pos = (
            self.x + TILE_SIZE // 2 + offset_x,
            self.y + TILE_SIZE // 2 + offset_y
        )
        
        tile_actor._surf = tile_actor._surf.subsurface(
            Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        )
        tile_actor.draw()


class Map:
    def __init__(self):
        self.base = []
        self.muros = []
        self.pilares = []
        self.map_width = 0
        self.map_height = 0

    def load(self):
        base_grid = load_csv("map/map_base.csv")
        muros_grid = load_csv("map/map_muros.csv")
        pilares_grid = load_csv("map/map_pilares.csv")
        
        # Calcular dimensões do mapa
        self.map_height = len(base_grid)
        self.map_width = len(base_grid[0]) if base_grid else 0
        
        self.base = self.grid_to_tiles(base_grid)
        self.muros = self.grid_to_tiles(muros_grid)
        self.pilares = self.grid_to_tiles(pilares_grid)

    def grid_to_tiles(self, grid):
        tiles = []
        for row_idx, row in enumerate(grid):
            for col_idx, tile_id in enumerate(row):
                if tile_id >= 0:
                    tile = Tile(tile_id, col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                    tiles.append(tile)
        return tiles

    def draw(self, screen_width, screen_height):
        # Calcular offset para centralizar o mapa
        offset_x = (screen_width - (self.map_width * TILE_SIZE)) // 2
        offset_y = (screen_height - (self.map_height * TILE_SIZE)) // 2
        
        for tile in self.base:
            tile.draw(offset_x, offset_y)
        for tile in self.muros:
            tile.draw(offset_x, offset_y)
        for tile in self.pilares:
            tile.draw(offset_x, offset_y)
