import pyglet
from pyglet import shapes
from units.oldguard import OldGuard
from units.oldguard import animate_waiting
from window.camera import Camera
from config.settings import *
from terrain.grid import Grid

class Window(pyglet.window.Window):

    def __init__(self, game):
        super(Window, self).__init__()
        # window.set_exclusive_mouse(self)
        Window.set_caption(self, caption="Napoléon ")
        Window.style = pyglet.window.Window.WINDOW_STYLE_DIALOG
        Window.set_fullscreen(self, fullscreen=True)

        cursor = Window.get_system_mouse_cursor(self, Window.CURSOR_CROSSHAIR)
        Window.set_mouse_cursor(self, cursor)
        self.batch = pyglet.graphics.Batch()
        self.game = game
        self.camera = Camera()


        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.middleground_group = pyglet.graphics.OrderedGroup(1)
        self.foreground_group = pyglet.graphics.OrderedGroup(2)


        self.grid = Grid(batch=self.batch,group=self.middleground_group)

        self.bandeau = []

        background_image = pyglet.resource.image('imgs/window/back.png')
        background_image.width = 4290
        background_image.height = 1300
        self.background = pyglet.sprite.Sprite(background_image,
                                               batch=self.batch, group=self.background_group)

        ### GEN ARMY :
        for i in range(12):
            if i%3 ==0:
                self.add_unit(OldGuard(line = i,row=i+1, batch=self.batch))

        self.move = False
        self.shoot = False

        self.init_bandeau()


    def init_bandeau(self):
        separator = 0
        for element in self.game.units:
            print(element)
            self.bandeau.append(
                (shapes.BorderedRectangle(LEFT_BORDER + separator, 0, BLOCKSIZE * 2, BLOCKSIZE * 1.7, border=3, color=(0, 0, 0),
                                          border_color=(0, 255, 0), batch=self.batch, group=self.foreground_group),

                 pyglet.sprite.Sprite(img=animate_waiting(), x=LEFT_BORDER, y=0,
                                      batch=self.batch, group=self.foreground_group)))
            separator +=150


    def get_element(self,x,y,action):
        element = self.grid.get_element(x,y,action)
        if element =="UNIT":
            ### DO SOMETHING UNIT HOVERED
            pass


    def main(self):
        if self.move :
            for unit in self.game.units :
                self.grid.unset_unit(unit)
                unit.move()
                self.grid.set_unit(unit)
        if self.shoot :
            for unit in self.game.units:
                unit.shoot()


    def add_unit(self, unit):
        self.game.add_unit(unit)
        self.grid.set_unit(unit)



    def update(self):
        self.label.x += self.camera.x
        self.label.text = str(self.camera.x)

    def on_draw(self):
        self.clear()
        self.main()
        self.batch.draw()
