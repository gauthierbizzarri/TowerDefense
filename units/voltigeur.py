import pyglet
from config.settings import *
import math
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import string
from terrain.grid import get_line_row
from pyglet import clock

def resize_image(image):
    image.height = BLOCKSIZE*1.5 * 1.2
    image.width = BLOCKSIZE * 1.8 *1.2
    return image


def center_image(image):
    # Center image at middle bottom of the image
    image.anchor_x = image.width // 8
    image.anchor_y = 0
    return image


image_waiting_a = pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/1.png')
image_waiting_b = pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/2.png')
image_waiting_c = pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/3.png')
image_waiting_d = pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/4.png')
image_waiting_e = pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/5.png')
image_waiting_f = pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/6.png')
image_waiting_g = pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/7.png')
image_waiting_h = pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/8.png')

image_shooting_a = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/1.png')
image_shooting_b = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/2.png')
image_shooting_c = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/3.png')
image_shooting_d = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/4.png')
image_shooting_e = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/5.png')
image_shooting_f = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/6.png')
image_shooting_g = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/7.png')
image_shooting_h = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/8.png')
image_shooting_i = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/9.png')
image_shooting_j = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/10.png')
image_shooting_k = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/11.png')
image_shooting_l = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/12.png')

image_marching_a = pyglet.resource.image('ressources/imgs/units/voltigeur/marching/1.png')
image_marching_b = pyglet.resource.image('ressources/imgs/units/voltigeur/marching/2.png')
image_marching_c = pyglet.resource.image('ressources/imgs/units/voltigeur/marching/3.png')
image_marching_d = pyglet.resource.image('ressources/imgs/units/voltigeur/marching/4.png')

image_bayonet_marching_a = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/1.png')
image_bayonet_marching_b = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/2.png')
image_bayonet_marching_c = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/3.png')
image_bayonet_marching_d = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/4.png')
image_bayonet_marching_e = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/5.png')
image_bayonet_marching_f = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/6.png')
image_bayonet_marching_g = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/7.png')
image_bayonet_marching_h = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/8.png')


def animate_waiting():
    frames = []
    for i in range(1, 9):
        img = pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/{}.png'.format(str((i))))
        img = resize_image(img)
        rdt = random.uniform(-1, 1)
        frame = pyglet.image.AnimationFrame(img, duration=0.33 + rdt)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "waiting "


def animate_shooting():
    frames = []
    for i in range(1, 13):
        if i == 12:
            img = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/{}.png'.format(str((i))))
            img = resize_image(img)
            rdt = random.uniform(-1, 1)
            frame = pyglet.image.AnimationFrame(img, duration=0.5+ rdt)
        else:
            img = pyglet.resource.image('ressources/imgs/units/voltigeur/shooting/{}.png'.format(str((i))))
            img = resize_image(img)
            rdt = random.uniform(-1, 1)
            frame = pyglet.image.AnimationFrame(img, duration=0.33 + rdt)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "shooting"


def animate_marching():
    frames = []
    for i in range(1, 5):
        img = pyglet.resource.image('ressources/imgs/units/voltigeur/marching/{}.png'.format(str((i))))
        img = resize_image(img)
        rdt = random.uniform(-1, 1)
        frame = pyglet.image.AnimationFrame(img, duration=0.1 +0)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "marching"

def animate_prepare_bayonet():
    frames = []
    for i in range(1, 5):
        img = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/{}.png'.format(str((i))))
        img = resize_image(img)
        rdt = random.uniform(-1, 1)
        frame = pyglet.image.AnimationFrame(img, duration=0.3 +rdt)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "prepare_bayonet"

def animate_marching_bayonet():
    frames = []
    for i in range(5, 9):
        img = pyglet.resource.image('ressources/imgs/units/voltigeur/bayonet_marching/{}.png'.format(str((i))))
        img = resize_image(img)
        rdt = random.uniform(-1, 1)
        frame = pyglet.image.AnimationFrame(img, duration=0.2 + rdt)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "marching_bayonet"

def animate_dying():
    frames = []
    for i in range(2, 4):
        img = pyglet.resource.image('ressources/imgs/units/voltigeur/dying/{}.png'.format(str((i))))
        img = resize_image(img)
        rdt = random.uniform(-1, 1)
        frame = pyglet.image.AnimationFrame(img, duration=0.3 +rdt)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "dying"
# voltigeur= center_image(voltigeur)

def place_unit_x(row):
    return BLOCKSIZE * row + LEFT_BORDER


def place_unit_y(line):
    return BLOCKSIZE * line + TOP_BORDER


def get_group(line):
    # LAYOUT
    return pyglet.graphics.OrderedGroup(abs(line - 13))


class EffectSprite(pyglet.sprite.Sprite):

    def set_name(self,name):
        self.name = name
    def __title__(self):
        return self.name

    def on_animation_end(self):
        if self.name =="shooting":
            self.image = animate_waiting()[0]
        if self.name =="dying":
            self.delete()
        if self.name =="prepare_bayonet":

            self.image = animate_marching_bayonet()[0]



class Voltigeur():
    def __init__(self, line, row, batch):
        self.line = line
        self.row = row
        self.image = EffectSprite(img=animate_waiting()[0], x=place_unit_x(self.row), y=place_unit_y(self.line),
                                  batch=batch, group=get_group(self.line))
        self.image.set_name(animate_waiting()[1])
        self.path_pos = 0
        self.path = []
        self.attitude = "waiting"
        self.type = "unit"
        self.id = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        self.x = place_unit_x(self.row)
        self.y = place_unit_y(self.line)
        self.player =pyglet.media.Player()
        self.name = "Voltigeur"
        self.bataillon = None
        self.is_selected = False
        self.bayonet = False

    def set_bataillon(self,bataillon):
        self.bataillon = bataillon

    def play_sound(self):
        self.player.play()
        self.player.next_source()

    def update_image(self):
        self.image.x = place_unit_x(self.row)
        self.image.y = place_unit_y(self.line)

    def add_path(self,matrix, end_line, end_row,etendard):
        if self.path != [] : return
        self.path = []
        end_line_1 = end_line    + self.line-etendard.line
        end_row_1 = end_row   + self.row -etendard.row
        grid = Grid(matrix=matrix)

        start = grid.node(int(self.row), int(self.line))
        end = grid.node(int(end_row_1), int(end_line_1))

        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)
        for element in path :
            self.path.append((place_unit_x(element[0]),place_unit_y(element[1])))

    def attack(self,target):
            self.attitude = "shooting"
            self.image.image = animate_shooting()[0]
            self.image.set_name(animate_shooting()[1])
            self.play_shooting_sound()

    def set_bayonet(self):
        self.image.image = animate_prepare_bayonet()[0]
        self.image.set_name(animate_prepare_bayonet()[1])
        self.bayonet = True


        # return


    def move(self):
        if self.path == []:
            return
        else:
            if self.bayonet:
                if self.attitude !="marching_bayonet":
                    self.attitude = "marching_bayonet"
                    self.image.image = animate_marching_bayonet()[0]
                    self.image.set_name(animate_marching_bayonet()[1])
            else :
                if self.attitude != "marching":
                        self.image.image = animate_marching()[0]
                        self.image.set_name(animate_marching()[1])
                        self.attitude = "marching"
        try:
            x1, y1 = self.path[self.path_pos]
            if self.path_pos + 1 >= len(self.path):
                self.path = []
                self.path_pos = 0
                if not self.bayonet:
                    self.attitude = "waiting"
                    self.image.image = animate_waiting()[0]
                    self.image.set_name(animate_waiting()[1])
                return
            x2, y2 = self.path[self.path_pos + 1]
            if True:
                dirn = ((x2 - x1), (y2 - y1))
                length = 1*math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
                dirn = (dirn[0] / length, dirn[1] / length)
                move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
                self.x = move_x
                self.y = move_y

                x = self.x - LEFT_BORDER
                y = self.y - TOP_BORDER
                row = x / BLOCKSIZE
                line = y / BLOCKSIZE

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

    def play_walking_sound(self):
        music = pyglet.resource.media('sounds/units/walking.mp3', streaming=False)
        self.player.queue(music)

    def play_shooting_sound(self):
        music = pyglet.resource.media('sounds/units/rifle_shoot.mp3', streaming=False)
        self.player.queue(music)

