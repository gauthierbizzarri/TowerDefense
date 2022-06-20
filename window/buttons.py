import pyglet
from pyglet import font
from pyglet import image
pyglet.resource.path = ['ressources']
pyglet.resource.reindex()
font.add_file('ressources/napo.ttf')
napo_font = font.load('ressources/napo.ttf', 16)



def get_img_from_name(name):
    units = {
        'OldGuard':  pyglet.resource.image('ressources/imgs/units/grenadier/waiting/1.png'),
        'Voltigeur' : pyglet.resource.image('ressources/imgs/units/voltigeur/waiting/1.png'),
    }
    frame = [pyglet.image.AnimationFrame(units[name], duration=0.33 ) ]
    ani = pyglet.image.Animation(frames=frame)
    return ani
class Button():
    def __init__(self,name,x,y,width,height,label,batch,group,color,line=None,row=None,batailon = None):
        self.name = name
        self.x = x
        self.y = y
        self.line = line
        self.row = row
        self.width = width
        self.height = height
        self.label = label
        self.batch = batch
        self.group = group
        self.color = color
        self.bataillon = batailon
        self.shape =  pyglet.shapes.Rectangle(self.x, self.y,self.width, self.height,self.color,self.batch,self.group)

        self.text = self.set_text(label)
        if self.name == "empty_case" or self.name == "OldGuard" or self.name == "Voltigeur":

            self.shape.color = (70,120,70)
            self.shape.opacity = 100
        else :
            self.shape.opacity = 120


    def set_img(self,name):
        self.image = pyglet.sprite.Sprite(img=get_img_from_name(name), x=self.x, y=self.y,
                                          batch=self.batch, group=pyglet.graphics.OrderedGroup(2))
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
                if self.name =="empty_case" or self.name =="OldGuard" or self.name =="Voltigeur" : return
                self.shape.opacity = 200
        else :
            if self.name == "empty_case" or self.name == "OldGuard" or self.name == "Voltigeur": return
            self.shape.opacity = 120


    def delete(self):
        self.text.delete()
        self.shape.delete()
        del(self)


class UnitButton():
    def __init__(self,name,x,y,width,height,label,batch,group,color,bataillon = None):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.batch = batch
        self.group = group
        self.color = color
        self.bataillon = bataillon

        self.image = pyglet.sprite.Sprite(img=get_img_from_name(self.name), x=x, y=y,
                                  batch=batch, group=self.group)


        self.shape =  pyglet.shapes.Rectangle(self.x, self.y,self.image.width, self.image.height,self.color,self.batch,self.group)

        self.shape.opacity = 0

        label = pyglet.text.Label(label,
                                  font_name='Napoleon Inline',
                                  font_size=36,
                                  x=1.1 * self.x, y=1.06 * self.y,
                                  batch=self.batch, group=pyglet.graphics.OrderedGroup(2))

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
                self.shape.opacity = 15
        else :
            self.shape.opacity = 0


    def delete(self):
        self.shape.delete()
        self.image.delete()
        del(self)

