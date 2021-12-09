import json

from pico2d import *
import game_framework
import game_world

from boy import Boy
from bg import Bg
from goomba import Goomba, Goomba_dead
from mushroom import Mushroom
from state_object import State_Object
import server

name = "MainState"

boy = None
statics = [State_Object() for i in range(33)]

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def enter():
    server.boy = Boy()
    game_world.add_object(server.boy, 1)

    server.goomba = Goomba()
    game_world.add_object(server.goomba, 1)

    server.background = Bg()
    game_world.add_object(server.background, 0)

    server.dead_goomba = Goomba_dead()

    server.mushroom = Mushroom()
    game_world.add_object(server.mushroom, 1)

    statics[0] = State_Object(896, 64, 64, 64)
    statics[1] = State_Object(1216, 64, 64, 96)
    statics[2] = State_Object(1472, 64, 64, 128)
    statics[3] = State_Object(1824, 64, 64, 128)
    statics[4] = State_Object(4288, 64, 32, 32)
    statics[5] = State_Object(4320, 64, 32, 64)
    statics[6] = State_Object(4352, 64, 32, 96)
    statics[7] = State_Object(4384, 64, 32, 128)
    statics[8] = State_Object(4480, 64, 32, 128)
    statics[9] = State_Object(4512, 64, 32, 96)
    statics[10] = State_Object(4544, 64, 32, 64)
    statics[11] = State_Object(4576, 64, 32, 32)
    statics[12] = State_Object(4736, 64, 32, 32)
    statics[13] = State_Object(4768, 64, 32, 64)
    statics[14] = State_Object(4800, 64, 32, 96)
    statics[15] = State_Object(4832, 64, 32, 128)
    statics[16] = State_Object(4864, 64, 32, 128)
    statics[17] = State_Object(4960, 64, 32, 128)
    statics[18] = State_Object(4992, 64, 32, 96)
    statics[19] = State_Object(5024, 64, 32, 64)
    statics[20] = State_Object(5056, 64, 32, 32)
    statics[21] = State_Object(5216, 64, 64, 64)
    statics[22] = State_Object(5728, 64, 32, 32)
    statics[23] = State_Object(5792, 64, 32, 32)
    statics[24] = State_Object(5824, 64, 32, 64)
    statics[25] = State_Object(5856, 64, 32, 96)
    statics[26] = State_Object(5888, 64, 32, 128)
    statics[27] = State_Object(5920, 64, 32, 160)
    statics[28] = State_Object(5952, 64, 32, 192)
    statics[29] = State_Object(5984, 64, 32, 224)
    statics[30] = State_Object(6016, 64, 32, 256)
    statics[31] = State_Object(6048, 64, 32, 256)

    for i in range(32):
        game_world.add_object(statics[i], 0)

    # with open('statics.json', 'r') as f:
    #     statics = json.load(f)

    # for data in statics:
    #     server.statics = State_Object(data['x'], data['y'], data['w'], data['h'])
    #     game_world.add_object(server.statics, 0)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            server.boy.handle_event(event)


def update():
    
    for game_object in game_world.all_objects():
        game_object.update()

    if server.dead_goomba in game_world.all_objects():
        if server.dead_goomba.timer == 0:
            game_world.remove_object(server.dead_goomba)

    for static in statics:
        if collide(static, server.mushroom):
            server.mushroom.dir *= -1
        if collide(static, server.boy):
            print('collied with statics')
            if static.y + static.height <= server.boy.land_y:
                server.boy.land_y = static.y + static.height
                break
            elif static.x > server.boy.x:
                server.boy.velocity = clamp(-RUN_SPEED_PPS, server.boy.velocity, 0)
                break
            elif static.x < server.boy.x:
                server.boy.velocity = clamp(0, server.boy.velocity, RUN_SPEED_PPS)
                break
    
    if collide(server.mushroom, server.boy):
        server.boy.state = 1
        server.mushroom.y += 500
        game_world.remove_object(server.mushroom)
            
            
    if collide(server.goomba, server.boy):
        if server.boy.y - 32 >= server.goomba.y:
            print('goomba killed')
            server.dead_goomba.x, server.dead_goomba.y = server.goomba.x, server.goomba.y - 8
            server.goomba.y += 500
            game_world.remove_object(server.goomba)
            game_world.add_object(server.dead_goomba, 1)

        else:
            if server.boy.state == 1:
                server.boy.state = 0
            print('Mario killed')



    # delay(0.1)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()