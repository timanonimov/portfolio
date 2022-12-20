import arcade
import animate
from constants import SCALING
import random

class Runman(animate.Animate):
    def __init__(self, window):
        super().__init__("runman/frame-01.gif", scale = SCALING)
        self.lives = 3
        self.left_textures = []
        self.right_textures = []
        for i in range(1,10):
            self.left_textures.append(arcade.load_texture(f"runman/frame-0{i}.gif", flipped_horizontally = False))
            self.right_textures.append(arcade.load_texture(f"runman/frame-0{i}.gif", flipped_horizontally = True))
        self.side = False
        self.window = window
        self.speed = random.randint(2,5)
        
    
    def update(self):
        if abs(self.center_x - self.window.bill.center_x)  < 600:
            if self.window.bill.center_x < self.center_x:
                self.change_x = -self.speed
                self.textures = self.left_textures
            else:
                self.change_x = self.speed
                self.textures = self.right_textures
        else:
            self.change_x = 0
        if arcade.check_for_collision(self, self.window.bill):
            self.window.bill.lives -= 3
            self.kill()
        if self.lives <= 0:
            self.kill()
