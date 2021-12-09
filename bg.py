from pico2d import *
import server

class Bg:
    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.image = load_image('res/World2.png')
        self.w = self.image.w
        self.h = self.image.h

    def update(self):
        self.window_left = clamp(0, int(server.boy.x) - server.background.canvas_width // 2 , server.background.w - server.background.canvas_width)
        self.window_bottom = clamp(0, int(server.boy.y) - server.background.canvas_height // 2, server.background.h - server.background.canvas_height)
        pass

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            server.background.canvas_width,
            server.background.canvas_height , 0, 0
            # self.window_left, self.window_bottom, 
            # 3376 * 2, 480 * 2, 0, -480
            )
        

    def handle_event(self, event):
        pass