import math
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from units.oldguard import OldGuard
from units.voltigeur import Voltigeur
from config.settings import *
def place_unit_x(row):
    return BLOCKSIZE * row + LEFT_BORDER


def place_unit_y(line):
    return BLOCKSIZE * line + TOP_BORDER

class Bataillon():

    def __init__(self,units,grid):
        self.units = units
        self.grid = grid

        ## create path spawn

    def create_path_spawn(self,matrix):
        for unit in self.units :
            unit.add_path_spawn(matrix)
    def move_bataillon(self):
        for unit in self.units:
            # CREATE PATH FOR UNIT :
            self.grid.unset_unit(unit)
            unit.move()
            self.grid.set_unit(unit)

    def set_bayonet(self):
        for unit in self.units:
            unit.set_bayonet()

    def shoot(self,target):
        if isinstance(target, Bataillon) :
            for unit in self.units:
                print(len(target.units))
                if len(target.units)>0:
                    unit.attack(target)

    def add_path(self,matrix, end_line, end_row,etendard):
        for unit in self.units :
            unit.add_path(matrix,end_line,end_row,etendard)
    def play_effect(self):
        for unit in self.units :
            unit.play_effect()

    def main(self):
        pass
    def be_attacked(self):
        for unit in self.units :
            unit.be_attacked()
