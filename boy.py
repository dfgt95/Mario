import game_framework
from pico2d import *

import server
import game_world

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)



# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3



# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE_DOWN, SPACE_UP = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP
}

# Boy States

class IdleState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        elif event == SPACE_DOWN and boy.jump_velocity == 0 and boy.move_count == 1:
            boy.jump_velocity = 1.0
        elif event == SPACE_UP:
            boy.jump_velocity = 0
            boy.move_count = 0
        boy.jump_velocity = clamp(0, boy.jump_velocity, 1.0)

    def exit(boy, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        boy.x += boy.velocity * game_framework.frame_time
        if boy.jump_velocity == 0 and boy.y > boy.land_y + boy.height / 2:
            boy.y -= 1.0
        if boy.y < boy.land_y + boy.height / 2 + 32 * 5 and boy.jump_velocity != 0 and boy.move_count == 1:
            boy.y += boy.jump_velocity
        if boy.jump_velocity == 1.0 and boy.y == boy.land_y + boy.height / 2 + 32 * 5: boy.jump_velocity = 0
        if boy.y == boy.land_y + boy.height / 2: boy.move_count = 1
        if boy.y == boy.land_y + boy.height / 2 + 32 * 5 - 1: 
            boy.jump_velocity = 0
            boy.move_count = 0
        if boy.land_y + (boy.height / 2) > boy.y:
            boy.y = boy.land_y + (boy.height / 2)

    def draw(boy):
        cx, cy = boy.x-server.background.window_left, boy.y-server.background.window_bottom
        if boy.state == 0 :
            if boy.y - boy.height / 2 != boy.land_y:
                if boy.dir == 1:
                    boy.image.clip_draw(359, 188 - 15, 16, 16, cx, cy, 32, 32)
                else:
                    boy.image.clip_draw(29, 188 - 15, 16, 16, cx, cy, 32, 32)

            elif boy.dir == 1:
                boy.image.clip_draw(209, 188 - 15, 16, 16, cx, cy, 32, 32)
            else:
                boy.image.clip_draw(180, 188 - 15, 16, 16, cx, cy, 32, 32)

        elif boy.state == 1:
            if boy.dir == 1:
                boy.image.clip_draw(209, 188 - 83, 16, 32, cx, cy, 32, 64)
            else:
                boy.image.clip_draw(180, 188 - 83, 16, 32, cx, cy, 32, 64)


class RunState:
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        elif event == SPACE_DOWN and boy.jump_velocity == 0 and boy.move_count == 1:
            boy.jump_velocity = 1.0
            print(boy.velocity)
        elif event == SPACE_UP:
            boy.jump_velocity = 0
            boy.move_count = 0
        boy.dir = clamp(-1, boy.velocity, 1)
        boy.jump_velocity = clamp(0, boy.jump_velocity, 1.0)

    def exit(boy, event):
        if event == SPACE_DOWN:
            pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        boy.x += boy.velocity * game_framework.frame_time
        if boy.jump_velocity == 0 and boy.y > boy.land_y + boy.height / 2:
            boy.y -= 1.0
        if boy.y < boy.land_y + boy.height / 2 + 32 * 5 and boy.jump_velocity != 0 and boy.move_count == 1:
            boy.y += boy.jump_velocity
        if boy.jump_velocity == 1.0 and boy.y == boy.land_y + boy.height / 2 + 32 * 5: boy.jump_velocity = 0
        if boy.y == boy.land_y + boy.height / 2: boy.move_count = 1
        if boy.y == boy.land_y + boy.height / 2 + 32 * 5 - 1: 
            boy.jump_velocity = 0
            boy.move_count = 0
        if boy.land_y + (boy.height / 2) > boy.y:
            boy.y = boy.land_y + (boy.height / 2)

      

    def draw(boy):
        cx, cy = boy.x - server.background.window_left, boy.y - server.background.window_bottom
        if boy.state == 0:
            if boy.y - boy.height / 2 != boy.land_y:
                if boy.dir == 1:
                    boy.image.clip_draw(359, 188 - 15, 16, 16, cx, cy, 32, 32)
                else:
                    boy.image.clip_draw(29, 188 - 15, 16, 16, cx, cy, 32, 32)
            elif boy.dir == 1:
                if int(boy.frame % 4)== 3:
                    boy.image.clip_draw(209 + (2) * 30, 188 - 15, 16, 16, cx, cy, 32, 32)
                else:
                    boy.image.clip_draw(209 + (int(boy.frame) + 1) * 30, 188 - 15, 16, 16, cx, cy, 32, 32)

            else:
                if int(boy.frame % 4)== 3:
                    boy.image.clip_draw(90 + (1) * 30, 188 - 15, 16, 32, cx, cy, 32, 32)
                else:
                    boy.image.clip_draw(90 + (int(boy.frame)) * 30, 188 - 15, 16, 32, cx, cy, 32, 32)
        elif boy.state == 1:
            if boy.dir == 1:
                if int(boy.frame % 4)== 3:
                    boy.image.clip_draw(209 + (2) * 30, 188 - 83, 16, 32, cx, cy, 32, 64)
                else:
                    boy.image.clip_draw(209 + (int(boy.frame) + 1) * 30, 188 - 83, 16, 32, cx, cy, 32, 64)

            else:
                if int(boy.frame % 4)== 3:
                    boy.image.clip_draw(90 + (1) * 30, 188 - 83, 16, 32, cx, cy, 32, 64)
                else:
                    boy.image.clip_draw(90 + (int(boy.frame)) * 30, 188 - 83, 16, 32, cx, cy, 32, 64)

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE_DOWN: IdleState, SPACE_UP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: RunState, RIGHT_DOWN: RunState, SPACE_DOWN: RunState, SPACE_UP: RunState}
}

class Boy:
    def __init__(self):
        
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('res/mario11.png')
        self.font = load_font('res/ENCR10B.TTF', 16)
        self.move_count = 1
        self.dir = 1
        self.velocity = 0
        self.jump_velocity = 0
        self.frame = 0
        self.land_y = 64
        self.height = 0
        self.state = 0      # 0 = small / 1 = large / 2 = fire
        if self.state == 0:
            self.height = 32        # large = 64
        else:
            self.height = 64
        self.x, self.y = 40, self.land_y + self.height/2
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def get_bb(self):
        return self.x - 16, self.y - 32, self.x + 16, self.y + 32

    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if self.state == 0:
            self.height = 32        # large = 64
        else:
            self.height = 64
        if self.y < self.land_y + self.height / 2:
            self.y = self.land_y + self.height / 2
        
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        self.x = clamp(1, self.x, server.background.w - 50)
 
    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

