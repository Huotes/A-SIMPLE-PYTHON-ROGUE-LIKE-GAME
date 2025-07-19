import math
from pygame import Rect
from config import *

class Weapon:
    def __init__(self, player):
        self.player = player
        self.angle = 0
        self.radius = 40
        self.image = Actor("weapon")

    def update(self):
        self.angle += 0.1
        self.x = self.player.x + math.cos(self.angle) * self.radius
        self.y = self.player.y + math.sin(self.angle) * self.radius
        self.image.pos = (self.x, self.y)

    def draw(self):
        self.image.draw()

    def get_rect(self):
        return Rect(self.x - 16, self.y - 16, 32, 32)
