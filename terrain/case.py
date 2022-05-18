from config.settings import *
from pyglet import shapes
class Case():
    def __init__(self,line,row,batch,group,content="NONE",width=BLOCKSIZE,height=BLOCKSIZE):
        self.line = line
        self.row = row
        self.width = width
        self.height = height
        self.batch = batch
        self.group = group
        self.content = content
        self.is_selected = False
        border_left = LEFT_BORDER
        border_top =TOP_BORDER
        shape = shapes.BorderedRectangle(self.get_x() + border_left , self.get_y()+border_top,BLOCKSIZE, BLOCKSIZE, border=3, color=(20, 10, 20),
                                     border_color=(0, 100, 0), batch=self.batch, group=self.group)
        shape.opacity = 128
        self.shape = shape



    def get_x(self,update=False):
        if not update:
            return self.row * BLOCKSIZE
        else :
            return self.row * BLOCKSIZE + LEFT_BORDER

    def get_y(self,update = False):
        if not update:
            return self.line * BLOCKSIZE
        else:
            return self.line * BLOCKSIZE + TOP_BORDER
    def get_content(self):
        return self.content
    def set_content(self,new_content):
        self.content = new_content

    def update(self):
        if self.is_selected:
            selected_color = 100
        else :
            selected_color = 0

        if self.content =="UNIT":
            shape =  shapes.BorderedRectangle(self.get_x(update=True), self.get_y(update=True), BLOCKSIZE, BLOCKSIZE, border=3, color=(0+selected_color, 50, 0),
                                     border_color=(255, 0, 0), batch=self.batch, group=self.group)
            shape.opacity = 100
            self.shape = shape

        if self.content =="NONE":
            shape =  shapes.BorderedRectangle(self.get_x(update=True), self.get_y(update=True), BLOCKSIZE, BLOCKSIZE, border=3, color=(0+selected_color, 0, 0),
                                     border_color=(255, 0, 0), batch=self.batch, group=self.group)
            shape.opacity = 100
            self.shape = shape

