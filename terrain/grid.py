from config.settings import *
from pyglet import shapes
from terrain.case import Case
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid as grid_path
from pathfinding.finder.a_star import AStarFinder

def get_line_row(x,y):
    x = x - LEFT_BORDER
    y = y - TOP_BORDER
    row = int(x//BLOCKSIZE)
    line = int(y//BLOCKSIZE)
    return line , row
class Grid():

    def __init__(self, batch,group):
        self.batch = batch
        self.group = group
        self.mat = self.create_grid()

    def set_unit(self,unit):
        ### A CANON IS BIGGER THAN COMMON UNITS
        if unit.name =="Canon":

            self.mat[int(unit.line)][int(unit.row)].set_content("UNIT",unit)
            self.mat[int(unit.line)][int(unit.row)].is_selected = unit.is_selected
            """self.mat[int(unit.line)][int(unit.row+1)].set_content("UNIT", unit)
            self.mat[int(unit.line)][int(unit.row+1)].is_selected = unit.is_selected
            self.mat[int(unit.line)][int(unit.row+2)].set_content("UNIT", unit)
            self.mat[int(unit.line)][int(unit.row+2)].is_selected = unit.is_selected"""
            self.mat[int(unit.line)][int(unit.row)].update()
        else :
            self.mat[int(unit.line)][int(unit.row)].set_content("UNIT", unit)
            self.mat[int(unit.line)][int(unit.row)].is_selected = unit.is_selected
            self.mat[int(unit.line)][int(unit.row)].update()
        # self.update()

    def unset_unit(self,unit):

        if unit.name == "Canon":

            self.mat[int(unit.line)][int(unit.row)].set_content("NONE", unit)
            self.mat[int(unit.line)][int(unit.row)].is_selected = unit.is_selected
            """self.mat[int(unit.line)][int(unit.row + 1)].set_content("NONE", unit)
            self.mat[int(unit.line)][int(unit.row+1)].is_selected = unit.is_selected
            self.mat[int(unit.line)][int(unit.row + 2)].set_content("NONE", unit)
            self.mat[int(unit.line)][int(unit.row+2)].is_selected = unit.is_selected"""
            self.mat[int(unit.line)][int(unit.row)].update()
        else:
            self.mat[int(unit.line)][int(unit.row)].set_content("NONE", unit)
            self.mat[int(unit.line)][int(unit.row)].is_selected = unit.is_selected
            self.mat[int(unit.line)][int(unit.row)].update()
        # self.update()
    def update(self):
        for i in range (len(self.mat)):
            for j in range (len(self.mat[0])):
                self.mat[i][j].update()


    def set_move_tile(self,line,row):
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                if self.mat[i][j].is_destination:
                    self.mat[i][j].is_destination = False
        self.mat[line][row].is_destination = True
        self.update()

    def get_matrix_for_path(self):
        matrix = []
        for line in range(len(self.mat)):
            rows = []
            for row in range(len(self.mat[0])):
                if self.mat[line][row].content == "OBSTACLE": # or self.mat[line][row].content == "UNIT" :
                    element = 0
                else :
                    element = 1
                rows.append(element)
            # print("ROW : {}".format(str(rows)))
            matrix.append(rows)
        return matrix
        self.update()


    def get_element(self,x,y,action=None):
        line,row = get_line_row(x,y)
        if line>=LIGNES or row >=COLONNES: return None
        for i in range (len(self.mat)):
            for j in range (len(self.mat[0])):
                if action =="CLICK":
                    self.mat[i][j].is_selected = False
                if action =="HOVER":
                    self.mat[i][j].is_hovered = False

        if action == "CLICK":
            self.mat[line][row].is_selected = True
            self.update()
            self.mat[line][row].unit
        if action == "HOVER":
            self.mat[line][row].is_hovered = True
            self.update()

        return self.mat[line][row].unit , self.mat[line][row].content

    def create_grid(self):
        ## create empty matrix
        mat = []
        for x in range(LIGNES):
            col = []
            for y in range(COLONNES):
                case = Case(line=x, row=y,batch = self.batch,group = self.group)
                col.append(case)
            mat.append(col)

        for i in range(LIGNES):
            if i !=5:
                mat[i][6].content = "OBSTACLE"


        ## Create targets
        mat[10][1].content = "TARGET"

        return mat

    def draw_bataillon_selected(self,bataillon):
        for unit in bataillon.units :
            pass
            # self.mat[int(unit.line)][int(unit.row)].is_selected=True

