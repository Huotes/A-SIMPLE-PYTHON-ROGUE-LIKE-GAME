import pgzrun
from player import Player
from enemy import Enemy

enemies = []
enemy_spawn_timer = 0
ENEMY_SPAWN_INTERVAL = 2.0  # segundos

WIDTH = 800
HEIGHT = 600

player = Player((WIDTH // 2, HEIGHT // 2))
mouse_pos = (0, 0)
mouse_buttons = (False, False, False)


def draw():
    screen.clear()
    for enemy in enemies:
        enemy.draw()
    player.draw()



def update(dt):
    global enemy_spawn_timer
    player.update(dt, mouse_pos, mouse_buttons)

    # Atualizar inimigos
    for enemy in enemies:
        enemy.update((player.x, player.y))

    # Colisão de magias com inimigos
    for spell in player.spells:
        spell_rect = spell.get_rect()
        for enemy in enemies:
            if spell_rect.colliderect(enemy.get_rect()):
                enemy.hit()
                # "desativar" a spell atingida (removemos depois)
                spell.actor.x = -1000  # gambiarra rápida

    # Remover inimigos mortos
    enemies[:] = [e for e in enemies if not e.is_dead()]

    # Spawn de novos inimigos
    enemy_spawn_timer += dt
    if enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL:
        enemies.append(Enemy((player.x, player.y)))
        enemy_spawn_timer = 0


def on_mouse_move(pos, rel, buttons):
    global mouse_pos, mouse_buttons
    mouse_pos = pos
    # buttons é um set
    mouse_buttons = (
        1 in buttons,  # botão esquerdo
        2 in buttons,  # botão meio
        3 in buttons,  # botão direito
    )


def on_mouse_down(pos, button):
    global mouse_buttons
    # atualizar o estado do botão
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
