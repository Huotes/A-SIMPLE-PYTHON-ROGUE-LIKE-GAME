from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pygame import Rect
from config import *


class Player:
    def __init__(self, pos):
        self.x, self.y = pos
        self.speed = PLAYER_SPEED
        self.frame = 0
        self.anim_timer = 0
        self.facing_left = False

        self.idle_images_right = [Actor(f"wizzard_f_idle_anim_f{i}") for i in range(4)]
        self.idle_images_left = [
            Actor(f"wizzard_f_idle_anim_f{i}_left") for i in range(4)
        ]
        self.run_images_right = [Actor(f"wizzard_f_run_anim_f{i}") for i in range(4)]
        self.run_images_left = [
            Actor(f"wizzard_f_run_anim_f{i}_left") for i in range(4)
        ]
        self.current_images = self.idle_images_right

    def update(self, dt, mouse_pos, mouse_buttons):
        dx, dy = 0, 0
        if keyboard.a:
            dx = -self.speed
            self.facing_left = True
        if keyboard.d:
            dx = self.speed
            self.facing_left = False
        if keyboard.w:
            dy = -self.speed
        if keyboard.s:
            dy = self.speed

        self.x += dx
        self.y += dy

        if dx != 0 or dy != 0:
            self.current_images = (
                self.run_images_left if self.facing_left else self.run_images_right
            )
        else:
            self.current_images = (
                self.idle_images_left if self.facing_left else self.idle_images_right
            )

        self.anim_timer += 1
        if self.anim_timer % 10 == 0:
            self.frame = (self.frame + 1) % len(self.current_images)

    def draw(self):
        sprite = self.current_images[self.frame]
        sprite.pos = (self.x, self.y)
        sprite.draw()

    def get_rect(self):
        return Rect(self.x - 16, self.y - 16, 32, 32)
