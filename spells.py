from pgzero.actor import Actor
from pygame import Rect
import math

WIDTH = 800
HEIGHT = 600


class Spell:
    SPEED = 5

    def __init__(self, start_pos, target_pos):
        self.actor = Actor("light_ball_spell")
        self.actor.pos = start_pos

        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        self.velocity = (dx / distance * self.SPEED, dy / distance * self.SPEED)

    def update(self, dt):
        self.actor.x += self.velocity[0]
        self.actor.y += self.velocity[1]

    def draw(self):
        self.actor.draw()

    def is_off_screen(self):
        return (
            self.actor.right < 0
            or self.actor.left > WIDTH
            or self.actor.bottom < 0
            or self.actor.top > HEIGHT
        )

    def get_rect(self):
        return Rect(self.actor.x - 8, self.actor.y - 8, 16, 16)
