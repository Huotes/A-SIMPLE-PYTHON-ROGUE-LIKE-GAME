from pgzero.actor import Actor
from pygame import Rect
import math
from config import WIDTH, HEIGHT


class Spell:
    """Representa uma magia lançada pelo jogador com movimento linear."""

    SPEED = 5
    SIZE = 16
    HALF_SIZE = SIZE // 2

    def __init__(self, start_pos, target_pos):
        """
        Inicializa a magia com posição inicial e cálculo da velocidade para
        alcançar a posição alvo.

        Args:
            start_pos (tuple): Posição inicial (x, y) da magia.
            target_pos (tuple): Posição alvo (x, y) para onde a magia se dirige.
        """
        self.actor = Actor("light_ball_spell")
        self.actor.pos = start_pos

        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)

        if distance == 0:
            # Evita divisão por zero; fica parada
            self.velocity = (0, 0)
        else:
            self.velocity = (dx / distance * self.SPEED, dy / distance * self.SPEED)

    def update(self, dt):
        """
        Atualiza a posição da magia com base na velocidade.

        Args:
            dt (float): Delta time (não utilizado atualmente, mas útil para futuras melhorias).
        """
        self.actor.x += self.velocity[0]
        self.actor.y += self.velocity[1]

    def draw(self):
        """Desenha a magia na tela."""
        self.actor.draw()

    def is_off_screen(self):
        """
        Verifica se a magia saiu da tela.

        Returns:
            bool: True se a magia está fora da tela, False caso contrário.
        """
        return (
            self.actor.right < 0
            or self.actor.left > WIDTH
            or self.actor.bottom < 0
            or self.actor.top > HEIGHT
        )

    def get_rect(self):
        """
        Retorna o retângulo de colisão da magia.

        Returns:
            pygame.Rect: Retângulo centralizado na posição da magia.
        """
        return Rect(
            self.actor.x - self.HALF_SIZE,
            self.actor.y - self.HALF_SIZE,
            self.SIZE,
            self.SIZE,
        )
