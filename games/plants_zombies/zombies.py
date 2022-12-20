import arcade
from pyglet import window
import animate
from constants import SCREEN_WIDTH, LAWNS_LEFT

class Zombie(animate.Animate):
    def __init__(self, image, health, row, center_y, window):
        super().__init__(image, scale=0.09)
        self.health = health
        self.row = row
        self.set_position(SCREEN_WIDTH, center_y)
        self.change_x = 0.2
        self.window = window
        self.eating = False
    
    def update(self):
        if not self.eating:
            self.center_x -= self.change_x
        if self.health <= 0:
            self.window.killed_zombies += 1
            self.window.attack_time -= 1
            self.kill()
        self.eating = False
        food = arcade.check_for_collision_with_list(self, self.window.plants)
        for plant in food:
            if self.row == plant.row:
                self.eating = True
                plant.health -= 0.5
        if self.center_x < LAWNS_LEFT:
            self.window.game = False

class OrdinaryZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__('zombies/zom1.png', 12, row, center_y, window)
        self.append_texture(arcade.load_texture(f'zombies/zom1.png'))
        self.append_texture(arcade.load_texture(f'zombies/zom2.png'))
    
class ConeHeadZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__('zombies/cone1.png', 20, row, center_y, window)
        self.append_texture(arcade.load_texture(f'zombies/cone1.png'))
        self.append_texture(arcade.load_texture(f'zombies/cone2.png'))

class BuckHeadZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__('zombies/buck1.png', 32, row, center_y, window)
        self.append_texture(arcade.load_texture(f'zombies/buck1.png'))
        self.append_texture(arcade.load_texture(f'zombies/buck2.png'))