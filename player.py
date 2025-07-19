from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pygame import Rect
from spells import Spell
from config import PLAYER_SPEED

PLAYER_SIZE = 32
PLAYER_HALF = PLAYER_SIZE // 2


class Player:
    """Representa o jogador, incluindo movimentação, animação, magias e estado."""

    def __init__(self, pos, sounds, area_rect):
        """
        Inicializa o jogador.

        Args:
            pos (tuple): Posição inicial (x, y).
            sounds (module): Referência aos sons do jogo.
            area_rect (Rect): Área válida de movimentação.
        """
        self.x, self.y = pos
        self.sounds = sounds
        self.area_rect = area_rect
        self.speed = PLAYER_SPEED

        # Estado de movimento e animação
        self.frame = 0
        self.anim_timer = 0
        self.facing_left = False
        self.current_images = []

        # Magias
        self.spells = []
        self.can_shoot = True

        # Vida
        self.max_hp = 6
        self.hp = self.max_hp
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.visible = True

        # Sprites
        self.idle_images_right = [Actor(f"wizzard_f_idle_anim_f{i}") for i in range(4)]
        self.idle_images_left = [
            Actor(f"wizzard_f_idle_anim_f{i}_left") for i in range(4)
        ]
        self.run_images_right = [Actor(f"wizzard_f_run_anim_f{i}") for i in range(4)]
        self.run_images_left = [
            Actor(f"wizzard_f_run_anim_f{i}_left") for i in range(4)
        ]

    def update(self, dt, mouse_pos, mouse_buttons):
        """
        Atualiza o estado do jogador por frame.

        Args:
            dt (float): Delta time.
            mouse_pos (tuple): Posição atual do mouse.
            mouse_buttons (tuple): Estado dos botões do mouse.
        """
        self.handle_input()
        self.animate()
        self.handle_spell_cast(mouse_pos, mouse_buttons)
        self.update_spells(dt)
        self.handle_invulnerability(dt)
        self.constrain_position()

    def handle_input(self):
        """Lida com a entrada do teclado para movimentação."""
        dx = (-self.speed if keyboard.a else 0) + (self.speed if keyboard.d else 0)
        dy = (-self.speed if keyboard.w else 0) + (self.speed if keyboard.s else 0)

        self.facing_left = dx < 0 if dx != 0 else self.facing_left
        self.x += dx
        self.y += dy

        if dx or dy:
            self.current_images = (
                self.run_images_left if self.facing_left else self.run_images_right
            )
        else:
            self.current_images = (
                self.idle_images_left if self.facing_left else self.idle_images_right
            )

    def animate(self):
        """Atualiza o frame de animação."""
        self.anim_timer += 1
        if self.anim_timer % 10 == 0:
            self.frame = (self.frame + 1) % len(self.current_images)

    def handle_spell_cast(self, target_pos, mouse_buttons):
        """
        Gera uma magia caso o botão esquerdo do mouse esteja pressionado.

        Args:
            target_pos (tuple): Posição do cursor do mouse.
            mouse_buttons (tuple): Estado dos botões do mouse.
        """
        if mouse_buttons[0] and self.can_shoot:
            self.cast_spell(target_pos)
            self.can_shoot = False
        elif not mouse_buttons[0]:
            self.can_shoot = True

    def update_spells(self, dt):
        """Atualiza as magias ativas e remove as que saíram da tela."""
        for spell in self.spells:
            spell.update(dt)
        self.spells = [spell for spell in self.spells if not spell.is_off_screen()]

    def handle_invulnerability(self, dt):
        """Atualiza o estado de invulnerabilidade (piscando)."""
        if not self.invulnerable:
            return

        self.invulnerable_timer -= dt
        if self.invulnerable_timer <= 0:
            self.invulnerable = False
            self.visible = True
        else:
            # Piscar a cada 0.1s
            self.visible = int(self.invulnerable_timer * 10) % 2 == 1

    def constrain_position(self):
        """Mantém o jogador dentro dos limites da área permitida."""
        min_x = self.area_rect.left + PLAYER_HALF
        max_x = self.area_rect.right - PLAYER_HALF
        min_y = self.area_rect.top + PLAYER_HALF
        max_y = self.area_rect.bottom - PLAYER_HALF

        self.x = max(min_x, min(self.x, max_x))
        self.y = max(min_y, min(self.y, max_y))

    def cast_spell(self, target_pos):
        """
        Cria uma nova magia na direção do cursor.

        Args:
            target_pos (tuple): Posição do alvo da magia.
        """
        spell = Spell((self.x, self.y), target_pos)
        self.spells.append(spell)
        self.sounds.light_spell.play()

    def take_damage(self):
        """Aplica dano ao jogador, ativando invulnerabilidade temporária."""
        if self.invulnerable:
            return

        self.hp -= 1
        self.invulnerable = True
        self.invulnerable_timer = 1.0
        self.sounds.retro_hurt.play()

    def draw(self):
        """Desenha o jogador e suas magias na tela."""
        if self.visible:
            sprite = self.current_images[self.frame]
            sprite.pos = (self.x, self.y)
            sprite.draw()

        for spell in self.spells:
            spell.draw()

    def get_rect(self):
        """Retorna o retângulo de colisão do jogador."""
        return Rect(
            self.x - PLAYER_HALF, self.y - PLAYER_HALF, PLAYER_SIZE, PLAYER_SIZE
        )
