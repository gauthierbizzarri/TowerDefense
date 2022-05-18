from pyglet.gl import glTranslatef

class Camera():
    def __init__(self):
        self.x = 0
        self.y = 0
    def move_left(self):
        self.x +=50
        glTranslatef(self.x, self.y, 0)
    def move_right(self):
        self.x -=50
        glTranslatef(self.x, self.y, 0)