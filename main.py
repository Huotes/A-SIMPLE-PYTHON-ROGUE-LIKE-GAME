import pgzrun
from player import Player
from enemy import Enemy
from config import WIDTH, HEIGHT
from pgzero.actor import Actor
from pygame import Rect

enemies = []
enemy_spawn_timer = 0
ENEMY_SPAWN_INTERVAL = 2.0  # segundos

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

mouse_pos = (0, 0)
mouse_buttons = (False, False, False)

game_over = False

score = 0
level_complete = False


def draw():
    screen.clear()
    map_image.draw()

    if not game_over:
        for enemy in enemies:
            enemy.draw()
        player.draw()
        draw_hearts()
        draw_score()
    if level_complete:
        draw_dark_overlay()
        draw_level_complete()
    elif game_over:
        draw_game_over_overlay()


def draw_score():
    screen.draw.text(
        f"Pontos: {score}",
        topleft=(20, 20),
        fontsize=36,
        color="white",
        shadow=(1, 1),
    )


def draw_hearts():
    full = Actor("ui_heart_full")
    half = Actor("ui_heart_half")
    empty = Actor("ui_heart_empty")

    heart_x = WIDTH - 20
    heart_y = 20
    hp = player.hp

    for i in range(3):
        if hp >= 2:
            icon = full
            hp -= 2
        elif hp == 1:
            icon = half
            hp -= 1
        else:
            icon = empty

        icon.topleft = (heart_x - i * 36, heart_y)
        icon.draw()


def draw_dark_overlay():
    overlay = screen.surface.copy()
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)  # 0 = transparente, 255 = opaco; 128 = 50% escuro
    screen.surface.blit(overlay, (0, 0))


def draw_game_over_overlay():
    screen.blit("mapa_montado", map_image.topleft)
    screen.surface.set_alpha(128)
    screen.fill((0, 0, 0))
    screen.surface.set_alpha(255)
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=60, color="white")
    screen.draw.text("Pressione ENTER para reiniciar", center=(WIDTH // 2, HEIGHT // 2 + 30), fontsize=30, color="gray")


def draw_level_complete():
    screen.draw.text(
        "NÍVEL COMPLETO!",
        center=(WIDTH // 2, HEIGHT // 2 - 50),
        fontsize=64,
        color="yellow",
        owidth=1.0,
        ocolor="black",
    )


def update(dt):
    global enemy_spawn_timer, game_over, score, level_complete

    if game_over or level_complete:
        return

    player.update(dt, mouse_pos, mouse_buttons)

    for enemy in enemies:
        enemy.update((player.x, player.y))

        # Colisão com o jogador
        if enemy.get_rect().colliderect(player.get_rect()):
            player.take_damage()

    # Colisão de magias
    for spell in player.spells:
        spell_rect = spell.get_rect()
        for enemy in enemies:
            if spell_rect.colliderect(enemy.get_rect()):
                was_dead = enemy.is_dead()
                enemy.hit()
                if not was_dead and enemy.is_dead():
                    score += 5
                    sounds.monster_death.play()
                spell.actor.x = -1000

    enemies[:] = [e for e in enemies if not e.is_dead()]

    enemy_spawn_timer += dt
    if enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL:
        enemies.append(Enemy((player.x, player.y)))
        enemy_spawn_timer = 0

    if player.hp <= 0:
        game_over = True
        sounds.loop_bg_sound.stop()
        sounds.game_over_sound.play(-1)

    if score >= 100:
        level_complete = True
        sounds.level_complete.play()


def restart_game():
    global player, enemies, score, game_over, enemy_spawn_timer, level_complete

    enemies = []
    enemy_spawn_timer = 0
    score = 0
    game_over = False
    level_complete = False

    player_start_x = offset_x + map_image_width // 2
    player_start_y = offset_y + map_image_height // 2
    player = Player((player_start_x, player_start_y), sounds, area_rect)

    sounds.game_over_sound.stop()
    sounds.loop_bg_sound.play(-1)


def on_mouse_move(pos, rel, buttons):
    global mouse_pos, mouse_buttons
    mouse_pos = pos
    mouse_buttons = (
        1 in buttons,
        2 in buttons,
        3 in buttons,
    )


def on_mouse_down(pos, button):
    global mouse_buttons
    if button == mouse.LEFT:
        mouse_buttons = (True, mouse_buttons[1], mouse_buttons[2])


def on_mouse_up(pos, button):
    global mouse_buttons
    if button == mouse.LEFT:
        mouse_buttons = (False, mouse_buttons[1], mouse_buttons[2])


def on_key_down(key):
    if game_over and key == keys.RETURN:
        restart_game()
    elif key == keys.K_1:
        player.weapon.switch("1")
    elif key == keys.K_2:
        player.weapon.switch("2")


sounds.loop_bg_sound.play(-1)
pgzrun.go()
