import math
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from units.oldguard import OldGuard
from units.voltigeur import Voltigeur
import random
from config.settings import *
def place_unit_x(row):
    return BLOCKSIZE * row + LEFT_BORDER


def place_unit_y(line):
    return BLOCKSIZE * line + TOP_BORDER

class Bataillon():

    def __init__(self,units):
        self.units = units
    def set_batch(self,batch):
        for unit in self.units :
            unit.set_batch(batch)

    def set_grid(self,grid):
        self.grid = grid




    def create_path_spawn(self,matrix):
        for unit in self.units :
            unit.add_path_spawn(matrix)
    def move_bataillon(self):

        for unit in self.units:
            if unit.health != 0:            # CREATE PATH FOR UNIT :
                self.grid.unset_unit(unit)
                unit.move()
                self.grid.set_unit(unit)

    def set_bayonet(self):
        for unit in self.units:
            unit.set_bayonet()

    def shoot(self,target):
        if isinstance(target, Bataillon) :

            for unit in self.units:

                if len(target.units) < 1:
                    unit.shoot = False
                target_unit = target.units[random.randint(0,len(target.units)-1)]
                unit.attack(target_unit)

    def add_path(self,matrix, end_line, end_row,etendard):
        for unit in self.units :
            unit.add_path(matrix,end_line,end_row,etendard)
    def play_effect(self):
        for unit in self.units :
            unit.play_effect()

    def main(self):
        for unit in self.units :
            if unit.image.name =="dead":
                self.units.remove(unit)
                unit.image.delete()

    def be_attacked(self):
        for unit in self.units :
            unit.be_attacked()
