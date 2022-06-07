

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
    image.height = BLOCKSIZE*0.8
    image.width = BLOCKSIZE *0.7
    return image

def center_image(image):
    # Center image at middle bottom of the image
    image.anchor_x = image.width // 8
    image.anchor_y = 0
    return image


image_ball1= pyglet.resource.image('ressources/imgs/misc/ball.png')


def image_ball():

    frames = []
    img = pyglet.resource.image('ressources/imgs/misc/ball.png')
    img = resize_image(img)
    frame = pyglet.image.AnimationFrame(img, duration=0.13)
    frames.append(frame)
    ani = pyglet.image.Animation(frames=frames)
    return ani, "waiting "

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
        pass
        # self.delete()



class Projectile():
    def __init__(self, line, row, batch,target):
        self.line = line
        self.row = row
        self.image = EffectSprite(img=image_ball()[0], x=place_unit_x(self.row), y=place_unit_y(self.line),
                                  batch=batch, group=get_group(self.line))
        self.path_pos = 0
        self.path = []
        self.id = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        self.x = place_unit_x(self.row)
        self.y = place_unit_y(self.line)
        self.player =pyglet.media.Player()
        self.is_selected = False
        self.name = "Projectile"
        self.bayonet = False
        self.stop = False
        self.target = target

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


        # return


    def move(self):
        try:
            # x1, y1 = self.path[self.path_pos]
            # x2, y2 = self.path[self.path_pos + 1]
            if True:
                dirn = ((self.target.x - self.x), (self.target.y - self.y))
                length = 1/6*math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
                if length < 1 :
                    self.stop = True
                    return
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

