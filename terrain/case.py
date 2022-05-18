from config.settings import *
from pyglet import shapes
class Case():
    def __init__(self,line,row,batch,group,content="border",width=BLOCKSIZE,height=BLOCKSIZE):
        self.line = line
        self.row = row
        self.width = width
        self.height = height
        self.batch = batch
        self.group = group
        self.content = content
        border_left = LEFT_BORDER
        border_top =TOP_BORDER
        shape = shapes.BorderedRectangle(self.get_x() + border_left , self.get_y()+border_top,BLOCKSIZE, BLOCKSIZE, border=3, color=(20, 10, 20),
                                     border_color=(0, 100, 0), batch=self.batch, group=self.group)
        shape.opacity = 128
        self.shape = shape



    def get_x(self):
        return self.row * BLOCKSIZE
    def get_y(self):
        return self.line * BLOCKSIZE
    def get_content(self):
        return self.content
    def set_content(self,new_content):
        self.content = new_content

    def draw(self):
        if self.content =="border":
            shapes.BorderedRectangle(self.get_x(), self.get_y(),BLOCKSIZE, BLOCKSIZE, border=1, color=(0, 0, 0),
                                     border_color=(255, 0, 0), batch=self.batch, group=self.group)