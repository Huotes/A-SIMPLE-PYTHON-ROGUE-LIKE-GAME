from enemy import Enemy
from config import *
import random

class GameManager:
    def __init__(self):
        self.level = 1

    def spawn_enemies(self):
        enemies = []
        for _ in range(ENEMIES_PER_LEVEL):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            enemies.append(Enemy((x, y)))
        return enemies

    def check_collisions(self, player, enemies):
        for enemy in enemies[:]:
            if enemy.get_rect().colliderect(player.weapon.get_rect()):
                sounds.hit.play()
                enemies.remove(enemy)

    def level_complete(self, enemies):
        return len(enemies) == 0

    def draw_ui(self):
        screen.draw.text(f"Level {self.level}", topleft=(10, 10), fontsize=30)
