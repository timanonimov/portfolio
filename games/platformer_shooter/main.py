import arcade
import bill
from constants import *
import line
import bullet
import runman
import random
import sniper
import live
import time


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, center_window=True)
        # Звуки
        self.coin_sound = arcade.load_sound('sounds/coin.wav')
        # Текустуры для фона
        self.background_textures = []
        for i in range(1, 16):
            self.background_textures.append(arcade.load_texture(f'background/Map{i}.png'))
        self.game_over = arcade.load_texture('game_over.jpg')
        self.end_game = arcade.load_texture('endgame.png')
        # Поля
        self.index_texture = 0
        self.game = True
        self.is_walk = False
        self.lines_for_level = []
        self.down_pressed = False
        self.runmans_for_level = []
        self.runmans_engine = []
        self.snipers_for_level = []
        self.win = False
        self.time_win = time.time()
        self.sound = arcade.load_sound('sounds/main_theme.mp3')
        self.music = arcade.play_sound(self.sound, volume=0.1)
        # Спрайты
        self.bill = bill.Bill()
        # Спрайтлисты
        self.lines = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.snipers = arcade.SpriteList()
        self.snipers_bullet = arcade.SpriteList()
        self.lives = arcade.SpriteList()
        # Инициализация спрайтов
        self.setup()
        # Физика
        self.engine = arcade.PhysicsEnginePlatformer(self.bill, self.lines, GRAVITY)

    def setup(self):
        for i in range(0, 801, 100):
            low_line = line.Line()
            low_line.set_position(i, 20)
            self.lines.append(low_line)
            low_line.visible = False
        for i, lines in enumerate(COORDS):
            self.lines_for_level.append([])
            self.runmans_for_level.append([])
            for x, y in lines:
                other_line = line.Line()
                other_line.set_position(x, y)
                self.lines_for_level[i].append(other_line)
                # runmans
                new_runman = runman.Runman(self)
                if x == -100:
                    new_runman.set_position(random.randint(50, SCREEN_WIDTH - 50), 100)
                else:
                    new_runman.set_position(x, y + 50)
                self.runmans_for_level[i].append(new_runman)
        for i, snipers in enumerate(COORDS_SNIPERS):
            self.snipers_for_level.append([])
            for x, y in snipers:
                new_sniper = sniper.Sniper(self)
                new_sniper.set_position(x, y)
                self.snipers_for_level[i].append(new_sniper)
        self.append_line(0)
        for i in range(self.bill.lives):
            bill_live = live.Live()
            bill_live.set_position(50 + 40 * i, SCREEN_HEIGHT - 50)
            self.lives.append(bill_live)

    def on_draw(self):
        if self.game:
            self.clear((255, 255, 255))
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                          self.background_textures[self.index_texture])
            self.bill.draw()
            self.lines.draw()
            self.bullets.draw()
            self.enemies.draw()
            self.snipers.draw()
            self.snipers_bullet.draw()
            self.lives.draw()
            if self.win and time.time() - self.time_win > 3:
                arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                              self.end_game)
        else:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                          self.game_over)

    def update(self, delta_time):
        if self.game:
            self.bill.update()
            if self.is_walk:
                self.bill.update_animation(delta_time)
            self.engine.update()
            if self.bill.back_left():
                if self.index_texture < len(self.background_textures) - 2:
                    self.index_texture += 1
                    self.append_line(-1)
            elif self.bill.back_right():
                if self.index_texture > 0:
                    self.index_texture -= 1
                    self.append_line(1)
            self.bullets.update()
            self.enemies.update_animation(delta_time)
            self.enemies.update()
            for runman_engine in self.runmans_engine:
                runman_engine.update()
            self.snipers.update()
            self.snipers_bullet.update()
            if self.bill.lives <= 0:
                self.game = False
            if self.index_texture == len(self.background_textures) - 2 and not len(self.snipers) and not len(
                    self.enemies):
                self.index_texture += 1
                self.win = True
                self.time_win = time.time()
            if self.sound.get_stream_position(self.music) == 0:
                self.music = arcade.play_sound(self.sound, 0.3)

    def append_line(self, side):
        self.append_runman(side)
        self.append_sniper(side)
        self.snipers_bullet = arcade.SpriteList()
        if side:
            for i in range(len(self.lines_for_level[self.index_texture + side])):
                self.lines.pop()
        for new_line in self.lines_for_level[self.index_texture]:
            self.lines.append(new_line)

    def append_runman(self, side):
        self.runmans_engine.clear()
        if side:
            for i in range(len(self.runmans_for_level[self.index_texture + side])):
                if len(self.enemies):
                    self.enemies.pop()
        for new_runman in self.runmans_for_level[self.index_texture]:
            self.enemies.append(new_runman)
            self.runmans_engine.append(arcade.PhysicsEnginePlatformer(new_runman, self.lines, GRAVITY))

    def append_sniper(self, side):
        if side:
            for i in range(len(self.snipers_for_level[self.index_texture + side])):
                if len(self.snipers):
                    self.snipers.pop()
        for new_sniper in self.snipers_for_level[self.index_texture]:
            self.snipers.append(new_sniper)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.is_walk = True
            self.bill.change_x = -PLAYER_MOVEMENT_SPEED
            self.bill.side = True
            self.bill.set_side()

        if key == arcade.key.RIGHT:
            self.is_walk = True
            self.bill.change_x = PLAYER_MOVEMENT_SPEED
            self.bill.side = False
            self.bill.set_side()

        if key == arcade.key.DOWN:
            self.bill.to_down()
            self.down_pressed = True

        if key == arcade.key.UP:
            if self.engine.can_jump():
                arcade.play_sound(self.bill.jump_sound)
                self.engine.jump(JUMP)

        if key == arcade.key.SPACE:
            new_bullet = bullet.Bullet(self)
            arcade.play_sound(new_bullet.shoot_sound)
            new_bullet.set_position(self.bill.center_x + 10, self.bill.center_y + 10)
            if self.down_pressed:
                new_bullet.center_y = self.bill.center_y - 15
            else:
                new_bullet.center_y = self.bill.center_y + 10
            self.bullets.append(new_bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.DOWN:
            self.bill.change_x = 0
            self.is_walk = False
            self.bill.set_texture(0)
            self.down_pressed = False


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
