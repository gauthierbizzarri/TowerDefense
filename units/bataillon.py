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
        for unit in self.units :
            unit.add_path(unit.line, unit.row + 3)

    def move_bataillon(self):
        for unit in self.units:
            # CREATE PATH FOR UNIT :
            self.grid.unset_unit(unit)
            unit.move()
            self.grid.set_unit(unit)

    def shoot(self):
        for unit in self.units:
            unit.shoot()

    def add_path(self,matrix, end_line=0, end_row=3):
        for unit in self.units :
            unit.path = []

            grid = Grid(matrix=matrix)

            start = grid.node(unit.line, unit.row)
            end = grid.node(unit.line+end_line, unit.rowend_row)
            finder = AStarFinder()
            path_astar, runs = finder.find_path(start, end, grid)

            precision = 10
            xf = place_unit_x(end_row)
            yf = place_unit_y(end_line)
            posx = place_unit_x(unit.row)
            posy = place_unit_y(unit.line)
            path = [(posx, posy)]
            unit.path = path
