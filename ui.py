from pygame import Rect
from config import *

buttons = {
    "start": Rect(300, 200, 200, 50),
    "sound": Rect(300, 270, 200, 50),
    "exit": Rect(300, 340, 200, 50)
}
sound_on = True

def draw_menu():
    screen.fill((20, 20, 30))
    screen.draw.text("Roguelike Game", center=(WIDTH//2, 100), fontsize=50)
    for name, rect in buttons.items():
        screen.draw.filled_rect(rect, (50, 50, 100))
        screen.draw.text(name.upper(), center=rect.center, fontsize=30)

def update_menu():
    pass

def handle_menu_click(pos):
    global sound_on
    if buttons["sound"].collidepoint(pos):
        sound_on = not sound_on
        sounds.click.play()
    elif buttons["exit"].collidepoint(pos):
        exit()

def button_clicked(name, pos):
    return buttons[name].collidepoint(pos)

def draw_game_over():
    screen.clear()
    screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60)

def draw_next_level():
    screen.clear()
    screen.draw.text("LEVEL CLEARED!", center=(WIDTH//2, HEIGHT//2), fontsize=60)
