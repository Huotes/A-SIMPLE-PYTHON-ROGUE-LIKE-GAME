import pgzrun
from pgzero.actor import Actor
from pygame import Rect

from config import WIDTH, HEIGHT
from player import Player
from enemy import Enemy


# --- Constantes e variáveis globais ---
ENEMY_SPAWN_INTERVAL = 2.0

enemies = []
enemy_spawn_timer = 0
mouse_pos = (0, 0)
mouse_buttons = (False, False, False)
game_over = False
score = 0
level_complete = False

# Mapa como imagem centralizada
map_image = Actor("mapa_montado")
map_image_width = map_image.width
map_image_height = map_image.height

# Calcular offset para centralizar o mapa
offset_x = (WIDTH - map_image_width) // 2
offset_y = (HEIGHT - map_image_height) // 2
map_image.topleft = (offset_x, offset_y)

# Posição inicial do player no centro do mapa renderizado
player_start_x = offset_x + map_image_width // 2
player_start_y = offset_y + map_image_height // 2

area_rect = Rect(offset_x, offset_y, map_image_width, map_image_height)
player = Player((player_start_x, player_start_y), sounds, area_rect)


# --- Funções de Desenho ---
def draw():
    """Desenha todos os elementos na tela com base no estado do jogo."""
    screen.clear()
    map_image.draw()

    if level_complete:
        draw_dark_overlay()
        draw_level_complete()
    elif game_over:
        draw_game_over_overlay()
    else:
        list(map(lambda e: e.draw(), enemies))
        player.draw()
        draw_hearts()
        draw_score()


def draw_score():
    """Exibe a pontuação atual na tela."""
    screen.draw.text(
        f"Pontos: {score}",
        topleft=(20, 20),
        fontsize=36,
        color="white",
        shadow=(1, 1),
    )


def draw_hearts():
    """Desenha os corações de vida do jogador."""
    icons = {
        2: Actor("ui_heart_full"),
        1: Actor("ui_heart_half"),
        0: Actor("ui_heart_empty")
    }

    heart_x = WIDTH - 20
    heart_y = 20
    hp = player.hp

    for i in range(3):
        icon = icons[2 if hp >= 2 else 1 if hp == 1 else 0]
        hp -= 2 if hp >= 2 else 1 if hp == 1 else 0
        icon.topleft = (heart_x - i * 36, heart_y)
        icon.draw()


def draw_dark_overlay():
    """Desenha uma sobreposição escura transparente (usado em tela de vitória)."""
    overlay = screen.surface.copy()
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)  # 0 = transparente, 255 = opaco; 128 = 50% escuro
    screen.surface.blit(overlay, (0, 0))


def draw_game_over_overlay():
    """Desenha a tela de game over com instruções para reiniciar."""
    screen.blit("mapa_montado", map_image.topleft)
    screen.surface.set_alpha(128)
    screen.fill((0, 0, 0))
    screen.surface.set_alpha(255)
    screen.draw.text(
        "GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=60, color="white"
    )
    screen.draw.text(
        "Pressione ENTER para reiniciar",
        center=(WIDTH // 2, HEIGHT // 2 + 30),
        fontsize=30,
        color="gray",
    )


def draw_level_complete():
    """Desenha a mensagem de vitória (nível completo)."""
    screen.draw.text(
        "NÍVEL COMPLETO!",
        center=(WIDTH // 2, HEIGHT // 2 - 50),
        fontsize=64,
        color="yellow",
        owidth=1.0,
        ocolor="black",
    )


# --- Atualização da lógica do jogo ---
def update(dt):
    """Atualiza a lógica do jogo por frame."""
    global enemy_spawn_timer, game_over, score, level_complete

    if game_over or level_complete:
        return

    player.update(dt, mouse_pos, mouse_buttons)

    # Atualiza inimigos e verifica colisão com o jogador
    list(map(lambda e: e.update((player.x, player.y)), enemies))
    if any(e.get_rect().colliderect(player.get_rect()) for e in enemies):
        player.take_damage()

    check_spell_hits()

    # Remove inimigos mortos
    enemies[:] = list(filter(lambda e: not e.is_dead(), enemies))

    # Spawn de novos inimigos
    enemy_spawn_timer += dt
    if enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL:
        enemies.append(Enemy((player.x, player.y)))
        enemy_spawn_timer = 0

    # Verifica derrota
    if player.hp <= 0:
        game_over = True
        sounds.loop_bg_sound.stop()
        sounds.game_over_sound.play(-1)

    # Verifica vitória
    if score >= 100:
        level_complete = True
        sounds.level_complete.play()


def check_spell_hits():
    """Verifica colisões entre magias e inimigos e aplica dano e pontuação."""
    global score

    for spell in player.spells:
        spell_rect = spell.get_rect()

        for enemy in filter(lambda e: spell_rect.colliderect(e.get_rect()), enemies):
            was_dead = enemy.is_dead()
            enemy.hit()
            if not was_dead and enemy.is_dead():
                score += 5
                sounds.monster_death.play()
            spell.actor.x = -1000


def restart_game():
    """Reinicia o estado do jogo após o game over."""
    global player, enemies, score, game_over, enemy_spawn_timer, level_complete

    enemies.clear()
    score = 0
    game_over = False
    level_complete = False
    enemy_spawn_timer = 0

    player_start = (offset_x + map_image_width // 2, offset_y + map_image_height // 2)
    player = Player(player_start, sounds, area_rect)

    sounds.game_over_sound.stop()
    sounds.loop_bg_sound.play(-1)


# --- Controles ---
def on_mouse_move(pos, buttons):
    """Atualiza a posição do mouse e os botões pressionados."""
    global mouse_pos, mouse_buttons
    mouse_pos = pos
    mouse_buttons = tuple(btn in buttons for btn in (1, 2, 3))


def on_mouse_down(pos, button):
    """Registra o clique do mouse como pressionado."""
    global mouse_buttons
    if button == mouse.LEFT:
        mouse_buttons = (True, mouse_buttons[1], mouse_buttons[2])


def on_mouse_up(pos, button):
    """Registra o clique do mouse como solto."""
    global mouse_buttons
    if button == mouse.LEFT:
        mouse_buttons = (False, mouse_buttons[1], mouse_buttons[2])


def on_key_down(key):
    """Gerencia entrada de teclado para reinício."""
    if game_over and key == keys.RETURN:
        restart_game()


# --- Inicialização ---
sounds.loop_bg_sound.play(-1)
pgzrun.go()
