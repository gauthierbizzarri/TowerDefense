from config.settings import *
from pyglet import shapes
from terrain.case import Case


class Grid():

    def __init__(self, batch,group):
        self.batch = batch
        self.group = group
        self.mat = self.create_grid()

    def set_unit(self,unit):

        self.mat[int(unit.line)][int(unit.row)].content = "UNIT"
        self.update()

    def unset_unit(self,unit):

        self.mat[int(unit.line)][int(unit.row)].content = "NONE"
        self.update()
    def update(self):
        for i in range (len(self.mat)):
            for j in range (len(self.mat[0])):
                self.mat[i][j].update()


    def create_grid(self):
        # GET grid size :
        mat = []
        for x in range(LIGNES):
            col = []
            for y in range(COLONNES):
                case = Case(line=x, row=y,batch = self.batch,group = self.group)
                col.append(case)
            mat.append(col)
        return mat

