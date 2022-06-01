import math
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from config.settings import *
def place_unit_x(row):
    return BLOCKSIZE * row + LEFT_BORDER


def place_unit_y(line):
    return BLOCKSIZE * line + TOP_BORDER

class Bataillon():

    def __init__(self,units,grid):
        self.units = units
        self.grid = grid
        # DEFINITION UNITE DE CENTRE DE GRAVITE
        # BATAILLON DE 6 GRENADIERS2

    def move_bataillon(self):
        for unit in self.units:
            # CREATE PATH FOR UNIT :
            # self.grid.unset_unit(unit)
            unit.move()
            # self.grid.set_unit(unit)

    def shoot(self):
        for unit in self.units:
            unit.shoot()

    def add_path(self,matrix, end_line, end_row,etendard):
        for unit in self.units :
            unit.add_path(matrix,end_line,end_row,etendard)
