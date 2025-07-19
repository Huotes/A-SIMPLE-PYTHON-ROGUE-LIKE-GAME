import pgzrun
from player import Player
from enemy import Enemy
from config import WIDTH, HEIGHT
from pgzero.actor import Actor

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

player = Player((player_start_x, player_start_y))

mouse_pos = (0, 0)
mouse_buttons = (False, False, False)


def draw():
    screen.clear()
    map_image.draw()
    for enemy in enemies:
        enemy.draw()
    player.draw()


def update(dt):
    global enemy_spawn_timer
    player.update(dt, mouse_pos, mouse_buttons)

    for enemy in enemies:
        enemy.update((player.x, player.y))

    for spell in player.spells:
        spell_rect = spell.get_rect()
        for enemy in enemies:
            if spell_rect.colliderect(enemy.get_rect()):
                enemy.hit()
                spell.actor.x = -1000

    enemies[:] = [e for e in enemies if not e.is_dead()]

    enemy_spawn_timer += dt
    if enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL:
        enemies.append(Enemy((player.x, player.y)))
        enemy_spawn_timer = 0


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
    if key == keys.K_1:
        player.weapon.switch("1")
    elif key == keys.K_2:
        player.weapon.switch("2")


pgzrun.go()
