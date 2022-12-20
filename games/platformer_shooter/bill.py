import arcade
import animate
from constants import *

class Bill(animate.Animate):
    def __init__(self):
        super().__init__("go_bill/0.gif",scale=SCALING)
        self.jump_sound = arcade.load_sound('sounds/jump.wav')
        self.center_x = 100
        self.center_y = 100
        self.left_textures = []
        self.right_textures = []
        for i in range(6):
            self.left_textures.append(arcade.load_texture(f"go_bill/{i}.gif", flipped_horizontally = True))
            self.right_textures.append(arcade.load_texture(f"go_bill/{i}.gif", flipped_horizontally = False))
        self.side = False
        self.right_down = arcade.load_texture('bill_textures/BillLayingDown.png', flipped_horizontally = False)
        self.left_down = arcade.load_texture('bill_textures/BillLayingDown.png', flipped_horizontally = True)
        self.lives = 3
        self.pain_sound = arcade.load_sound('sounds/pain.wav')


    def set_side(self):
        if self.side:
            self.textures = self.left_textures
        else:
            self.textures = self.right_textures
    
    def to_down(self):
        if self.side:
            self.texture = self.left_down
        else:
            self.texture = self.right_down

    def back_left(self):
        if self.left > SCREEN_WIDTH:
            self.center_x = 0
            return True
        return False
    
    def back_right(self):
        if self.right < 0:
            self.center_x = SCREEN_WIDTH
            return True
        return False

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.lives <= 0:
            self.kill()


