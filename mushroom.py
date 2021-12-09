import game_framework
from pico2d import *
import server

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 7.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

class Mushroom:          
    def __init__(self, dir = 1):
        self.image = load_image('res/Items.png')
        self.x, self.y = 300, 120 #673, 208
        self.dir = dir
        self.speed = RUN_SPEED_PPS
        self.fall_speed = 0.5

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def update(self):
        self.y -= self.fall_speed
        if self.y <= 80: self.fall_speed = 0
        if self.dir == 1:
            self.x += self.speed * game_framework.frame_time
        else:
            self.x -= self.speed * game_framework.frame_time

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(0, 524-24, 16, 16, cx, cy, 32, 32)
