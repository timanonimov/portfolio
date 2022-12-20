import arcade

class Bullet(arcade.Sprite):
    def __init__(self, window):
        super().__init__('bullet.png', 0.03)
        self.shoot_sound = arcade.load_sound('sounds/shoot.wav')
        self.window = window
        if self.window.bill.side:
            self.change_x = -25
        else:
            self.change_x = 25

    def update(self):
        self.center_x += self.change_x
        if abs(self.center_x - self.window.bill.center_x)  > 300:
            self.kill()
        snipers = arcade.check_for_collision_with_list(self, self.window.snipers)
        for sniper in snipers:
            sniper.lives -= 1
            arcade.play_sound(self.window.coin_sound)
        runmans = arcade.check_for_collision_with_list(self, self.window.enemies)
        for runman in runmans:
            runman.lives -= 1
            arcade.play_sound(self.window.coin_sound)          
        if len(snipers) > 0 or len(runmans) > 0:
            self.kill()

class SniperBullet(Bullet):
    def __init__(self, window, direction_x, direction_y, x, y):
        super().__init__(window)
        self.set_position(x, y + 10)
        self.change_x = direction_x
        self.change_y = direction_y
        self.created = x

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if abs(self.center_x - self.created) > 300:
            self.kill()
        if arcade.check_for_collision(self, self.window.bill):
            self.window.bill.lives -= 1
            self.kill()
            arcade.play_sound(self.window.bill.pain_sound)
            self.window.lives.pop()

    

    

        