import pgzrun
from player import Player

WIDTH = 800
HEIGHT = 600

player = Player((WIDTH // 2, HEIGHT // 2))
mouse_pos = (0, 0)
mouse_buttons = (False, False, False)


def draw():
    screen.clear()
    player.draw()


def update(dt):
    player.update(dt, mouse_pos, mouse_buttons)


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
