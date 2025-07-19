import random
from pygame import Rect
from config import *

class Enemy:
    def __init__(self, pos):
        self.x, self.y = pos
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.frame = 0
        self.images_idle = [Actor(f'enemy_idle_{i}') for i in range(4)]
        self.speed = ENEMY_SPEED

    def update(self):
        if self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed
        elif self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed

        if random.randint(0, 60) == 0:
            self.direction = random.choice(['left', 'right', 'up', 'down'])

        self.frame = (self.frame + 1) % len(self.images_idle)

    def draw(self):
        img = self.images_idle[self.frame]
        img.pos = (self.x, self.y)
        img.draw()

    def get_rect(self):
        return Rect(self.x - 16, self.y - 16, 32, 32)
