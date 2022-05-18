from config.settings import *
from pyglet import shapes
from terrain.case import Case


class Grid():

    def __init__(self, batch,group):
        self.batch = batch
        self.group = group
        self.grid = self.create_grid()

    def create_grid(self):
        # GET grid size :
        Mat = []
        for x in range(LIGNES):
            col = []
            for y in range(COLONNES):
                case = Case(line=x, row=y,batch = self.batch,group = self.group).shape
                col.append(case)
            Mat.append(col)
        return Mat

