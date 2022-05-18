import pyglet
from pyglet import shapes
from units.oldguard import OldGuard
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


        # LAYOUT 0 : BACKGROUND
        # LAYOUT 1 : GRID
        # LAYOUT 2 : LINE 12 ................
        # LAYOUT 3 : LINE 11 ................
        # LAYOUT 14: LINE 0

        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.middleground_group = pyglet.graphics.OrderedGroup(1)
        self.foreground_group = pyglet.graphics.OrderedGroup(2)


        self.grid = Grid(batch=self.batch,group=self.middleground_group).grid


        background_image = pyglet.resource.image('imgs/window/back.png')
        background_image.width = 4290
        background_image.height = 1300
        self.background = pyglet.sprite.Sprite(background_image,
                                               batch=self.batch, group=self.background_group)


        ### GEN ARMY :
        for i in range(12):
            self.add_unit(OldGuard(line = i,row=0, batch=self.batch))


    def add_unit(self, unit):
        self.game.add_unit(unit)


    def update(self):
        self.label.x += self.camera.x
        self.label.text = str(self.camera.x)
    def on_draw(self):
        self.clear()
        self.batch.draw()
