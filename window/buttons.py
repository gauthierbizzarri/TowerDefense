import pyglet
from pyglet import font
pyglet.resource.path = ['ressources']
pyglet.resource.reindex()
font.add_file('ressources/napo.ttf')
napo_font = font.load('ressources/napo.ttf', 16)


class Button():
    def __init__(self,name,x,y,width,height,label,batch,group,color):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.batch = batch
        self.group = group
        self.color = color
        self.shape =  pyglet.shapes.Rectangle(self.x, self.y,self.width, self.height,self.color,self.batch,self.group)

        self.text = self.set_text(label)

        self.shape.opacity = 120



    def set_text(self,label):
        label = pyglet.text.Label(label,
                                  font_name='Napoleon Inline',
                                  font_size=36,
                                  x=1.1 * self.x, y=1.06 * self.y,
                                  batch=self.batch, group=pyglet.graphics.OrderedGroup(2))
        return label
    def is_pressed(self,x,y):
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False

    def is_hovered(self,x,y):
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                self.shape.opacity = 200
        else :
            self.shape.opacity = 120


    def delete(self):
        self.text.delete()
        self.shape.delete()
        del(self)


