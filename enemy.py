import random
import math
from pgzero.actor import Actor
from pygame import Rect
from config import *

WIDTH = 800
HEIGHT = 600

class Enemy:
    def __init__(self, player_pos):
        self.x, self.y = self.spawn_outside_screen()
        self.frame = 0
        self.anim_timer = 0
        self.hp = 4
        self.speed = ENEMY_SPEED

        # Carregar animações
        self.idle_images_right = [Actor(f"masked_orc_idle_anim_f{i}") for i in range(4)]
        self.idle_images_left = [Actor(f"masked_orc_idle_anim_f{i}_left") for i in range(4)]
        self.run_images_right = [Actor(f"masked_orc_run_anim_f{i}") for i in range(4)]
        self.run_images_left = [Actor(f"masked_orc_run_anim_f{i}_left") for i in range(4)]

        self.current_images = self.idle_images_right
        self.facing_left = False

    def spawn_outside_screen(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return (random.randint(0, WIDTH), -32)
        elif side == "bottom":
            return (random.randint(0, WIDTH), HEIGHT + 32)
        elif side == "left":
            return (-32, random.randint(0, HEIGHT))
        else:
            return (WIDTH + 32, random.randint(0, HEIGHT))

    def update(self, player_pos):
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            vel_x = (dx / dist) * self.speed
            vel_y = (dy / dist) * self.speed
            self.x += vel_x
            self.y += vel_y

            # Animação de movimento esquerda/direita
            self.facing_left = vel_x < 0
            self.current_images = (
                self.run_images_left if self.facing_left else self.run_images_right
            )
        else:
            # Está exatamente na posição do player
            self.current_images = (
                self.idle_images_left if self.facing_left else self.idle_images_right
            )

        self.anim_timer += 1
        if self.anim_timer % 10 == 0:
            self.frame = (self.frame + 1) % len(self.current_images)

    def draw(self):
        img = self.current_images[self.frame]
        img.pos = (self.x, self.y)
        img.draw()

    def get_rect(self):
        return Rect(self.x - 16, self.y - 16, 32, 32)

    def hit(self):
        self.hp -= 1

    def is_dead(self):
        return self.hp <= 0
