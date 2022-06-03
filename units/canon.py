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
    image.height = BLOCKSIZE*1.5 * 1.4
    image.width = BLOCKSIZE * 1.8 *2.6
    return image

def center_image(image):
    # Center image at middle bottom of the image
    image.anchor_x = image.width // 8
    image.anchor_y = 0
    return image


image_waiting_a = pyglet.resource.image('ressources/imgs/units/canon/reloading/1.png')

image_shooting = []
for i in range(1,46):
    image = pyglet.resource.image('ressources/imgs/units/canon/reloading/{}.png'.format(str(i)))
    image_shooting.append(image)


def animate_waiting():
    frames = []
    img = pyglet.resource.image('ressources/imgs/units/canon/reloading/{}.png'.format(str((1))))
    img = resize_image(img)
    frame = pyglet.image.AnimationFrame(img, duration=0.13)
    frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "waiting "


def animate_shooting():
    frames = []
    for i in range(1, 45):
        if i == 28:
            img = pyglet.resource.image('ressources/imgs/units/canon/reloading/{}.png'.format(str((i))))
            img = resize_image(img)
            frame = pyglet.image.AnimationFrame(img, duration=0.5)
        else:
            img = pyglet.resource.image('ressources/imgs/units/canon/reloading/{}.png'.format(str((i))))
            img = resize_image(img)
            frame = pyglet.image.AnimationFrame(img, duration=0.13)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "shooting"


def animate_marching():
    frames = []
    img = pyglet.resource.image('ressources/imgs/units/canon/reloading/1.png'.format(str((i))))
    img = resize_image(img)
    frame = pyglet.image.AnimationFrame(img, duration=0.1)
    frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "marching"





def animate_dying():
    frames = []
    for i in range(2, 4):
        img = pyglet.resource.image('ressources/imgs/units/grenadier/dying/{}.png'.format(str((i))))
        img = resize_image(img)
        frame = pyglet.image.AnimationFrame(img, duration=0.3)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani, "dying"
# grenadier= center_image(grenadier)

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



class Canon():
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
        self.is_selected = False
        self.bataillon = None
        self.name = "Canon"
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

    def attack(self):
        if self.attitude != "shooting":
            self.attitude = "shooting"
            self.image.image = animate_shooting()[0]
            self.image.set_name(animate_shooting()[1])
            self.play_shooting_sound()

    def set_bayonet(self):
        return
        self.image.image = animate_prepare_bayonet()[0]
        self.image.set_name(animate_prepare_bayonet()[1])
        self.bayonet = True


        # return


    def move(self):
        if self.path == []:
            return
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
                length = 1/10*math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
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

