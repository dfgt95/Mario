from pico2d import *
import game_world
import game_framework
import server

class State_Object:
    def __init__(self, x = 0, y = 0, w = 0, h = 0):
        self.x, self.y = x, y
        self.width = w
        self.height = h
        self.cx, self.cy = 0, 0

    def get_bb(self):
        self.cx, self.cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return self.x, self.y, self.x + self.width, self.y + self.height

    def draw(self):
        pass
        # fill here for draw

    def update(self):
        pass