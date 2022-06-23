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

def place_unit_x(row):
    return BLOCKSIZE * row + LEFT_BORDER


def place_unit_y(line):
    return BLOCKSIZE * line + TOP_BORDER


class Unit():
    def __init__(self, line, row, batch):
        self.batch = batch
        self.dest_line = line
        self.dest_row = row+5
        self.line = line
        self.row = row -5

        self.has_spawned = False


        self.effect = None
        self.path_pos = 0
        self.path = []
        self.path_spawn = []
        self.path_spawn_pos = 0
        self.attitude = "waiting"
        self.type = "unit"
        self.id = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        self.x = place_unit_x(self.row)
        self.y = place_unit_y(self.line)
        self.player =pyglet.media.Player()
        self.bataillon = None
        self.is_selected = False
        self.bayonet = False
        self.health = 1
        self.shoot = False
        self.target = None

    def set_batch(self,batch):
        self.batch = batch
        self.image.batch = batch

    def set_bataillon(self,bataillon):
        self.bataillon = bataillon

    def play_sound(self):
        self.player.play()
        self.player.next_source()

    def update_image(self):
        self.image.x = place_unit_x(self.row)
        self.image.y = place_unit_y(self.line)

    def add_path_spawn(self,matrix):
        if self.path_spawn != [] : return
        self.path_spawn = []
        end_line_1 = self.dest_line
        end_row_1 = self.dest_row
        grid = Grid(matrix=matrix)

        start = grid.node(0, int(self.line))
        end = grid.node(int(end_row_1), int(end_line_1))

        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)
        for element in path :
            self.path_spawn.append((place_unit_x(element[0]),place_unit_y(element[1])))
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

    def attack(self,target=None):
        if self.target == None:
            self.target = target
        if self.image.name =="waiting" or self.image.name =="marching":
            self.attitude = "prepare_shooting"
            self.image.image = animate_prepare_shooting()[0]
            self.image.set_name(animate_prepare_shooting()[1])
        self.shoot = True
        if self.image.name =="shooting" :
            try:
                self.target.be_attacked()
                self.target = None
            except:
                pass

    def be_attacked(self):
        self.image.image = animate_dying()[0]
        self.image.set_name(animate_dying()[1])
        self.health = self.health - 1

    def set_bayonet(self):
        self.image.image = animate_prepare_bayonet()[0]
        self.image.set_name(animate_prepare_bayonet()[1])
        self.bayonet = True


    def spawn(self):
        if self.path_spawn == []:
            self.line = self.dest_line
            self.row = self.dest_row
            self.has_spawned = True
            return
        else:
            if self.bayonet:
                if self.attitude != "marching_bayonet":
                    self.attitude = "marching_bayonet"
                    self.image.image = animate_marching_bayonet()[0]
                    self.image.set_name(animate_marching_bayonet()[1])
            else:
                if self.attitude != "marching":
                    self.image.image = animate_marching()[0]
                    self.image.set_name(animate_marching()[1])
                    self.attitude = "marching"
            x1, y1 = self.path_spawn[self.path_spawn_pos]
            if self.path_spawn_pos + 1 >= len(self.path_spawn):
                self.path_spawn = []
                self.path_spawn_pos = 0
                if not self.bayonet:
                    self.attitude = "waiting"
                    self.image.image = animate_waiting()[0]
                    self.image.set_name(animate_waiting()[1])
                return
            x2, y2 = self.path_spawn[self.path_spawn_pos + 1]
            dirn = ((x2 - x1), (y2 - y1))
            length = 1/3 * math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
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
                        self.path_spawn_pos += 1
                else:
                    if self.x >= x2 and self.y <= y2:
                        self.path_spawn_pos += 1
            else:  # moving left
                if dirn[1] >= 0:  # moving down
                    if self.x <= x2 and self.y >= y2:
                        self.path_spawn_pos += 1
                else:
                    if self.x <= x2 and self.y >= y2:
                        self.path_spawn_pos += 1
        self.update_image()


    def move(self):
        if not self.has_spawned:
            self.spawn()
        if self.shoot:
            self.attack()
        if self.path == [] :
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


    def play_effect(self):
        if self.image.name == "shooting":
            if self.effect is  None or self.effect.name =="smoke_ended" :
                self.effect = EffectSprite(img=animate_smoke()[0], x=place_unit_x(self.row)-10, y=place_unit_y(self.line),
                                         batch=self.batch, group=get_group(self.line+1))

                self.effect.set_name("smoke")


