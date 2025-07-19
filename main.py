import os
import pgzrun
from player import Player
from config import *

os.environ['PGZERO_ASSETS'] = 'assets'

player = Player((WIDTH // 2, HEIGHT // 2))

def draw():
    screen.clear()
    player.draw()

def update(dt):
    player.update(dt)

pgzrun.go()
