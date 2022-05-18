import attitude as attitude
import pyglet
from config.settings import *
import math

def center_image(image):
    # Center image at middle bottom of the image
    image.anchor_x = image.width // 8
    image.anchor_y = 0
    return image


image_waiting_a = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/1.png')
image_waiting_b = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/2.png')
image_waiting_c = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/3.png')
image_waiting_d = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/4.png')
image_waiting_e = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/5.png')
image_waiting_f = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/6.png')
image_waiting_g = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/7.png')
image_waiting_h = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/8.png')

image_shooting_a = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/1.png')
image_shooting_b = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/2.png')
image_shooting_c = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/3.png')
image_shooting_d = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/4.png')
image_shooting_e = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/5.png')
image_shooting_f = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/6.png')
image_shooting_g = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/7.png')
image_shooting_h = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/8.png')
image_shooting_i = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/9.png')
image_shooting_j = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/10.png')
image_shooting_k = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/11.png')
image_shooting_l = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/12.png')


image_marching_a = pyglet.resource.image('ressources/imgs/units/grenadier/marching/1.png')
image_marching_b = pyglet.resource.image('ressources/imgs/units/grenadier/marching/2.png')
image_marching_c = pyglet.resource.image('ressources/imgs/units/grenadier/marching/3.png')
image_marching_d = pyglet.resource.image('ressources/imgs/units/grenadier/marching/4.png')


def animate_waiting():
    frames = []
    for i in range(1,9):
        img = pyglet.resource.image('ressources/imgs/units/grenadier/waiting/{}.png'.format(str((i))))
        frame = pyglet.image.AnimationFrame(img, duration=0.33)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani

def animate_shooting():
    frames = []
    for i in range(1,13):
        if i == 12:
            img = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/{}.png'.format(str((i))))
            frame = pyglet.image.AnimationFrame(img, duration=5.7)
        else :
            img = pyglet.resource.image('ressources/imgs/units/grenadier/shooting/{}.png'.format(str((i))))
            frame = pyglet.image.AnimationFrame(img, duration=0.33)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani

def animate_marching():
    frames = []
    for i in range(1,5):
        img = pyglet.resource.image('ressources/imgs/units/grenadier/marching/{}.png'.format(str((i))))
        frame = pyglet.image.AnimationFrame(img, duration=0.22)
        frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
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
        self.image =  pyglet.sprite.Sprite(img=animate_waiting(), x=place_unit_x(self.row), y=place_unit_y(self.line),batch=batch,group=get_group(self.line))
        self.path_pos = 0
        self.path = []
        self.attitude= "waiting"


    def gen_path(self):
        lignes = LIGNES
        colonnes = COLONNES
        all_path = []
        for l in range(lignes):
            new_path = []
            for c in range(colonnes):
                new_path.append((place_unit_x(c), place_unit_y(l)))
            all_path.append(new_path)
        return all_path[self.line]

    def update_image(self):
        self.image.x = place_unit_x(self.row)
        self.image.y = place_unit_y(self.line)


    def shoot(self):
        if self.attitude!="shooting":
            self.image.image=animate_shooting()
            self.attitude = "shooting"


    def move(self):
        # UNSET POSITION

        if int(self.row) ==5:
            self.shoot()
            return
        if self.attitude!="marching":
            self.image.image=animate_marching()
            self.attitude = "marching"
        if self.row <COLONNES and self.line<LIGNES:
            self.row = self.row + 0.09
            self.update_image()




