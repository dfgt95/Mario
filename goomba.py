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
FRAMES_PER_ACTION = 2

class Goomba:          
    def __init__(self):
        self.image = load_image('res/Enemies_copy.png')
        self.x, self.y = 150, 64 + 16
        self.dir = -1
        self.speed = 10
        self.frame = 0

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * game_framework.frame_time

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        if self.dir == -1:
            if int(self.frame % 2) == 1:
                self.image.clip_draw(0, 508-32, 16, 16, cx, cy, 32, 32)
            else:
                self.image.clip_draw(18, 508-32, 16, 16, cx, cy, 32, 32)

class Goomba_dead:
    def __init__(self):
        self.image = load_image('res/Enemies_copy.png')
        self.x, self.y = 150, 64 + 16
        self.dir = -1
        self.speed = 10
        self.frame = 0
        self.timer = 50
    
    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(36, 508-32, 16, 8, cx, cy, 32, 16)
    
    def get_bb(self):
        return self.x - 16, self.y - 8, self.x + 16, self.y + 8

    def update(self):
        self.timer -= 1