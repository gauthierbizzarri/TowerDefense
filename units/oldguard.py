import pyglet
from config.settings import *


def center_image(image):
    # Center image at middle bottom of the image
    image.anchor_x = image.width // 8
    image.anchor_y = 0
    return image


image_a = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/1.png')
image_b = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/2.png')
image_c = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/3.png')
image_d = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/4.png')
image_e = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/5.png')
image_f = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/6.png')
image_g = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/7.png')
image_h = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/8.png')

def animate():
    frame_a = pyglet.image.AnimationFrame(image_a, duration=0.3)
    frame_b = pyglet.image.AnimationFrame(image_b, duration=0.2)
    frame_c = pyglet.image.AnimationFrame(image_c, duration=0.3)
    frame_d = pyglet.image.AnimationFrame(image_d, duration=0.3)
    frame_e = pyglet.image.AnimationFrame(image_e, duration=0.3)
    frame_f = pyglet.image.AnimationFrame(image_f, duration=0.3)
    frame_g = pyglet.image.AnimationFrame(image_g, duration=0.3)
    frame_h = pyglet.image.AnimationFrame(image_h, duration=0.3)
    ani = pyglet.image.Animation(frames=[frame_a, frame_b, frame_c,frame_d,frame_e,frame_d,frame_e,frame_f,frame_g,frame_h])
    return ani
# grenadier= center_image(grenadier)

def place_unit_x(row):
    return BLOCKSIZE*row +LEFT_BORDER
def place_unit_y(line):
    return BLOCKSIZE * line  + TOP_BORDER
def get_group(line):
    # LAYOUT
    return pyglet.graphics.OrderedGroup(abs(line-13))
class OldGuard():
    def __init__(self,line,row,batch):
        self.line = line
        self.row = row
        self.image =  pyglet.sprite.Sprite(img=animate(), x=place_unit_x(self.row), y=place_unit_y(self.line),batch=batch,group=get_group(self.line))



