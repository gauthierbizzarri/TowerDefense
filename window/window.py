import pyglet
from pyglet import shapes
from units.oldguard import OldGuard
from units.oldguard import animate_waiting
from window.camera import Camera
from config.settings import *
from terrain.grid import Grid
from terrain.grid import get_line_row

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

        self.clicked_unit = None
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
            self.bandeau.append(
                (shapes.BorderedRectangle(LEFT_BORDER + separator, 0, BLOCKSIZE * 1., BLOCKSIZE * 1.5, border=3, color=(0, 0, 0),
                                          border_color=(0, 255, 0), batch=self.batch, group=self.foreground_group),

                 pyglet.sprite.Sprite(img=animate_waiting()[0], x=LEFT_BORDER + separator , y=0,
                                      batch=self.batch, group=self.foreground_group)))
            separator +=BLOCKSIZE+20


    def get_element(self,x,y,action):
        element = self.grid.get_element(x,y,action)[0]
        if action =="CLICK":
            if element is not None :
                self.clicked_unit = element


    def handle_left(self,x,y):
        content = self.grid.get_element(x, y)[1]

        if self.clicked_unit :
            ### CHECK FREE :
            if content == "NONE":
                # UNSET OLD  MOVE TILE
                self.grid.set_move_tile(get_line_row(x,y)[0],get_line_row(x,y)[1])
                ###MOVE UNIT
                self.grid.unset_unit(self.clicked_unit)
                self.clicked_unit.add_path(get_line_row(x,y)[0],get_line_row(x,y)[1])
                self.grid.set_unit(self.clicked_unit)
            if content == "TARGET":
                # self.grid.set_move_tile(get_line_row(x, y)[0], get_line_row(x, y)[1])
                self.clicked_unit.attack()


    def main(self):
        """
       for unit in self.game.units :
            self.grid.unset_unit(unit)
            unit.move(unit.line,unit.row+2)
            self.grid.set_unit(unit)
            """
        self.init_bandeau()
        self.grid.create_matrix_for_path()
        for unit in self.game.units :
            self.grid.unset_unit(unit)
            unit.move()
            unit.play_sound()
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
