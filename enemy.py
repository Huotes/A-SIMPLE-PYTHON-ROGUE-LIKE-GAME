import random
import math
from pgzero.actor import Actor
from pygame import Rect
from config import ENEMY_SPEED

WIDTH = 800
HEIGHT = 600
ENEMY_SIZE = 32
ENEMY_HALF = ENEMY_SIZE // 2


class Enemy:
    """Inimigo que persegue o jogador com animação e colisão."""

    def __init__(self, player_pos):
        """
        Inicializa o inimigo fora da tela e carrega as animações.

        Args:
            player_pos (tuple): Posição atual do jogador.
        """
        self.x, self.y = self._spawn_outside_screen()
        self.frame = 0
        self.anim_timer = 0
        self.hp = 4
        self.speed = ENEMY_SPEED
        self.facing_left = False

        # Carrega animações
        self.idle_images_right = [Actor(f"masked_orc_idle_anim_f{i}") for i in range(4)]
        self.idle_images_left = [
            Actor(f"masked_orc_idle_anim_f{i}_left") for i in range(4)
        ]
        self.run_images_right = [Actor(f"masked_orc_run_anim_f{i}") for i in range(4)]
        self.run_images_left = [
            Actor(f"masked_orc_run_anim_f{i}_left") for i in range(4)
        ]

        self.current_images = self.idle_images_right

    def _spawn_outside_screen(self):
        """Define a posição inicial fora da tela, em um dos lados."""
        spawn_map = {
            "top": lambda: (random.randint(0, WIDTH), -ENEMY_SIZE),
            "bottom": lambda: (random.randint(0, WIDTH), HEIGHT + ENEMY_SIZE),
            "left": lambda: (-ENEMY_SIZE, random.randint(0, HEIGHT)),
            "right": lambda: (WIDTH + ENEMY_SIZE, random.randint(0, HEIGHT)),
        }
        side = random.choice(list(spawn_map.keys()))
        return spawn_map[side]()

    def update(self, player_pos):
        """
        Atualiza posição e animação do inimigo, indo na direção do jogador.

        Args:
            player_pos (tuple): Posição atual do jogador.
        """
        dx, dy = player_pos[0] - self.x, player_pos[1] - self.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            vel_x, vel_y = self._get_velocity_towards(dx, dy, dist)
            self.x += vel_x
            self.y += vel_y
            self.facing_left = vel_x < 0
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

    def _get_velocity_towards(self, dx, dy, dist):
        """
        Calcula a velocidade normalizada para seguir o jogador.

        Args:
            dx (float): Diferença em X.
            dy (float): Diferença em Y.
            dist (float): Distância total ao jogador.

        Returns:
            tuple: Velocidade (x, y)
        """
        return (dx / dist) * self.speed, (dy / dist) * self.speed

    def draw(self):
        """Desenha o inimigo com base no frame atual."""
        img = self.current_images[self.frame]
        img.pos = (self.x, self.y)
        img.draw()

    def get_rect(self):
        """Retorna o retângulo de colisão do inimigo."""
        return Rect(self.x - ENEMY_HALF, self.y - ENEMY_HALF, ENEMY_SIZE, ENEMY_SIZE)

    def hit(self):
        """Reduz a vida do inimigo em 1 ponto."""
        self.hp -= 1

    def is_dead(self):
        """Verifica se o inimigo foi derrotado."""
        return self.hp <= 0
