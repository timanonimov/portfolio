import arcade
import animate
import time
import sun
from constants import SCREEN_WIDTH
class Plant(animate.Animate):
    def __init__(self, image, health, cost, window):
        super().__init__(image, 0.12)
        self.health = health
        self.cost = cost
        self.row = 0
        self.column = 0
        self.window = window
        

    def update(self):
        if self.health <= 0:
            self.kill()
            self.window.lawns.remove((self.row, self.column))


    def planting(self, center_x, center_y, row, column):
        self.set_position(center_x, center_y)
        self.row = row
        self.column = column

class SunFlower(Plant):
    def __init__(self, window):
        super().__init__('plants/sun1.png', 80, 50, window)
        self.append_texture(arcade.load_texture('plants/sun1.png'))
        self.append_texture(arcade.load_texture('plants/sun2.png'))
        self.sun_spawn_time = time.time()
        self.window = window
    def update(self):
        super().update()
        if time.time() - self.sun_spawn_time >= 15:
            new_sun = sun.Sun(self.right, self.top)
            self.sun_spawn_time = time.time()
            self.window.spawn_suns.append(new_sun)
        self.window.spawn_suns.update()

class PeaShooter(Plant):
    def __init__(self, window):
        super().__init__('plants/pea1.png', 100, 100, window)
        for i in range(3):
            self.append_texture(arcade.load_texture(f'plants/pea{i+1}.png'))
        self.pea_spawn_time = time.time()
        self.window = window
    
    def update(self):
        super().update()
        zombie_on_line = False
        for zombie in self.window.zombie_list:
            if zombie.row == self.row:
                zombie_on_line = True
                break
        if time.time() - self.pea_spawn_time >= 2 and zombie_on_line:
            new_pea = Pea(self.right, self.top, self.window)
            self.pea_spawn_time = time.time()
            self.window.peas.append(new_pea)

class Pea(arcade.Sprite):
    def __init__(self, center_x, center_y, window):
        super().__init__('items/bul.png', 0.12)
        self.set_position(center_x, center_y)
        self.change_x = 7
        self.damage = 1
        self.window = window
    
    def update(self):
        super().update()
        self.center_x += self.change_x
        if self.center_x > SCREEN_WIDTH:
            self.kill()
        zombies = arcade.check_for_collision_with_list(self, self.window.zombie_list)
        for zombie in zombies:
            zombie.health -= self.damage
            self.kill()

class WallNut(Plant):
    def __init__(self, window):
        super().__init__('plants/nut1.png', 200, 50, window)
        for i in range(1,4):
            self.append_texture(arcade.load_texture(f'plants/nut{i}.png'))

class TorchWood(Plant):
    def __init__(self, window):
        super().__init__('plants/tree1.png', 120, 75, window)
        for i in range(1,4):
            self.append_texture(arcade.load_texture(f'plants/tree{i}.png'))
        self.window = window
    
    def update(self):
        super().update()
        fire_peas = arcade.check_for_collision_with_list(self, self.window.peas)
        for pea in fire_peas:
            pea.texture = arcade.load_texture('items/firebul.png')
            pea.damage = 3