import attitude as attitude
import pyglet
from config.settings import *
import math
import random
import time
import string
from terrain.grid import  get_line_row
from pyglet import clock
def center_image(image):
    # Center image at middle bottom of the image
    image.anchor_x = image.width // 8
    image.anchor_y = 0
    return image


image_waiting_a = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/1.png')
image_waiting_b = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/2.png')
image_waiting_c = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/3.png')
image_waiting_d = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/4.png')
image_waiting_e = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/5.png')
image_waiting_f = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/6.png')
image_waiting_g = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/7.png')
image_waiting_h = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/8.png')

image_shooting_a = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/1.png')
image_shooting_b = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/2.png')
image_shooting_c = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/3.png')
image_shooting_d = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/4.png')
image_shooting_e = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/5.png')
image_shooting_f = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/6.png')
image_shooting_g = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/7.png')
image_shooting_h = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/8.png')
image_shooting_i = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/9.png')
image_shooting_j = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/10.png')
image_shooting_k = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/11.png')
image_shooting_l = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/12.png')


image_marching_a = pyglet.resource.image('ressources/imgs/units/grenadier/marching/1.png')
image_marching_b = pyglet.resource.image('ressources/imgs/units/grenadier/marching/2.png')
image_marching_c = pyglet.resource.image('ressources/imgs/units/grenadier/marching/3.png')
image_marching_d = pyglet.resource.image('ressources/imgs/units/grenadier/marching/4.png')


def animate_waiting():
    frames = []
    for i in range(1,9):
        img = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/{}.png'.format(str((i))))
        frame = pyglet.image.AnimationFrame(img, duration=0.33)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "waiting "

def animate_shooting():
    frames = []
    for i in range(1,13):
        if i == 12:
            img = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/{}.png'.format(str((i))))
            frame = pyglet.image.AnimationFrame(img, duration=3)
        else :
            img = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/{}.png'.format(str((i))))
            frame = pyglet.image.AnimationFrame(img, duration=0.33)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani , "shooting"

def animate_marching():
    frames = []
    for i in range(1,5):
        img = pyglet.resource.image('ressources/imgs/units/grenadier/marching/{}.png'.format(str((i))))
        frame = pyglet.image.AnimationFrame(img, duration=0.1)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani , "marching"



# grenadier= center_image(grenadier)

def place_unit_x(row):
    return BLOCKSIZE*row +LEFT_BORDER
def place_unit_y(line):
    return BLOCKSIZE * line  + TOP_BORDER
def get_group(line):
    # LAYOUT
    return pyglet.graphics.OrderedGroup(abs(line-13))


class EffectSprite(pyglet.sprite.Sprite):

    def on_animation_end(self):
        if self.image =
        self.image = animate_shooting()


class OldGuard():
    def __init__(self,line,row,batch):
        self.line = line
        self.row = row
        self.image =  EffectSprite(img=animate_waiting(), x=place_unit_x(self.row), y=place_unit_y(self.line),batch=batch,group=get_group(self.line))
        self.path_pos = 0
        self.path = []
        self.attitude= "waiting"
        self.type = "unit"
        self.id = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        self.x = place_unit_x(self.row)
        self.y =  place_unit_y(self.line)

    def on_animation_end(self):
        print("ANIMATION END  CALLED ")
        self.attitude = "shooting"
        self.image.image = animate_waiting()


    def gen_path(self):
        all_path = []
        precision = 5
        for l in range(LIGNES):
            new_path = []
            for c in range(COLONNES):
                for i in range(precision):
                    new_path.append((place_unit_x(c)/precision, place_unit_y(l)/precision))
            all_path.append(new_path)
        return all_path[self.line]

    def update_image(self):
        self.image.x = place_unit_x(self.row)
        self.image.y = place_unit_y(self.line)




    def add_path(self,end_line,end_row):
        self.path = []
        precision = 10
        xf = place_unit_x(end_row)
        yf = place_unit_y(end_line)
        posx = place_unit_x(self.row)
        posy = place_unit_y(self.line)
        path = [(posx,posy)]
        distance = math.sqrt((posx - xf) ** 2 + (posy - yf) ** 2)
        for i in range(int(distance / BLOCKSIZE)):
            for j in range(precision):
                if xf - posx < 0:
                    posx = posx - BLOCKSIZE/precision
                if xf - posx > 0:
                    posx = posx + BLOCKSIZE/precision
                if yf - posy < 0:
                    posy = posy - BLOCKSIZE/precision
                if yf - posy > 0:
                    posy = posy + BLOCKSIZE/precision
                path.append((posx, posy))
        self.path = path

    def attack(self):
        if self.attitude != "shooting":
            self.attitude = "shooting"
            self.image.image = animate_shooting()

        # return

    def move(self):
        if self.path == []:

            return
        if self.attitude != "marching":
            self.image.image = animate_marching()
            self.attitude = "marching"
        try:
            x1, y1 = self.path[self.path_pos]
            if self.path_pos + 1 >= len(self.path):
                self.path = []
                self.path_pos = 0
                self.attitude = "waiting"
                self.image.image = animate_waiting()
                return
            x2, y2 = self.path[self.path_pos + 1]
            if True:
                dirn = ((x2 - x1), (y2 - y1))
                length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2) *1/4
                dirn = (dirn[0] / length, dirn[1] / length)
                move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
                self.x = move_x
                self.y = move_y

                x = self.x - LEFT_BORDER
                y = self.y - TOP_BORDER
                row = x / BLOCKSIZE
                line = y  / BLOCKSIZE

                self.line = line
                self.row = row
                # Go to next point
                if dirn[0] >= 0:  # moving right
                    if dirn[1] >= 0:  # moving down
                        if self.x >= x2 and self.y >= y2:
                            self.path_pos += 1
                    else:
                        if self.x >= x2 and self.y <= y2:
                            self.path_pos += 1
                else:  # moving left
                    if dirn[1] >= 0:  # moving down
                        if self.x <= x2 and self.y >= y2:
                            self.path_pos += 1
                    else:
                        if self.x <= x2 and self.y >= y2:
                            self.path_pos += 1
                self.update_image()
        except:
            pass






