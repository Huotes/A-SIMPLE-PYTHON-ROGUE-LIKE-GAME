from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pygame import Rect
from spells import Spell
from config import *


class Player:
    def __init__(self, pos):
        self.x, self.y = pos
        self.speed = PLAYER_SPEED
        self.frame = 0
        self.anim_timer = 0
        self.facing_left = False

        self.spells = []
        self.can_shoot = (
            True  # controle simples para não disparar múltiplas vezes por clique
        )

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

        # Magia: clique com botão esquerdo (índice 0)
        if mouse_buttons[0] and self.can_shoot:
            self.cast_spell(mouse_pos)
            self.can_shoot = False
        elif not mouse_buttons[0]:
            self.can_shoot = True

        # Atualizar magias
        for spell in self.spells:
            spell.update(dt)
        self.spells = [s for s in self.spells if not s.is_off_screen()]

    def cast_spell(self, target_pos):
        spell = Spell((self.x, self.y), target_pos)
        self.spells.append(spell)

    def draw(self):
        sprite = self.current_images[self.frame]
        sprite.pos = (self.x, self.y)
        sprite.draw()
        for spell in self.spells:
            spell.draw()

    def get_rect(self):
        return Rect(self.x - 16, self.y - 16, 32, 32)
