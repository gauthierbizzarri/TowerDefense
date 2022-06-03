import pyglet
from pyglet import shapes
from units.oldguard import OldGuard
from units.voltigeur import Voltigeur
from units.canon import Canon
from units.oldguard import animate_waiting
from window.camera import Camera
from config.settings import *
from terrain.grid import Grid
from terrain.grid import get_line_row
from units.bataillon import Bataillon

image= pyglet.resource.image('ressources/imgs/bataillon.png')

def img_bataillon():
    frames = []
    img = pyglet.resource.image('ressources/imgs/bataillon.png')
    frame = pyglet.image.AnimationFrame(img, duration=0.5)
    frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani



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



        self.move = False
        self.shoot = False


        self.clicked_bataillon = None


        self.bataillons = []


        self.init_armee()


        self.init_bandeau()
        self.grid.update()


    def init_bandeau(self):
        separator = 0
        for element in self.bataillons:
            self.bandeau.append(
               #  (shapes.BorderedRectangle(LEFT_BORDER + separator, 0,100  ,110,  border=3, color=(0, 0, 0),
                #                          border_color=(0, 255, 0), batch=self.batch, group=self.foreground_group),

                 pyglet.sprite.Sprite(img=img_bataillon(), x=LEFT_BORDER + separator , y=0,
                                      batch=self.batch, group=self.foreground_group))
            separator +=BLOCKSIZE+100


    def get_element(self,x,y,action):
        element = self.grid.get_element(x,y,action)[0]
        if action =="CLICK":
            if element is not None :
                self.clicked_unit = element
                self.clicked_bataillon = self.bataillons[self.clicked_unit.bataillon]

    def handle_right(self,x,y):
        self.get_element(x,y,action="CLICK")
    def handle_left(self,x,y):
        content = self.grid.get_element(x, y)[1]

        if self.clicked_unit :
            self.clicked_bataillon = self.bataillons[self.clicked_unit.bataillon]
            ### CHECK FREE :
            if content == "NONE":
                # UNSET OLD  MOVE TILE
                # self.grid.set_move_tile(get_line_row(x,y)[0],get_line_row(x,y)[1])
                ###MOVE UNIT
                #self.grid.unset_unit(self.clicked_unit)
                self.clicked_bataillon.add_path(self.grid.get_matrix_for_path(),get_line_row(x,y)[0],get_line_row(x,y)[1],self.clicked_unit)
                # self.grid.set_unit(self.clicked_unit)
            if content == "TARGET":
                # self.grid.set_move_tile(get_line_row(x, y)[0], get_line_row(x, y)[1])
                self.clicked_bataillon.shoot()

    def init_armee(self):
        ### GEN ARMY :
        # CENTRE GRAVITE BATAILLON

        ### 1 er Bataillon :

        l = 5
        r = 5
        units = [
            Voltigeur(line=l,        row=r,          batch=self.batch),
            Voltigeur(line=l,        row=r + 1,      batch=self.batch),
            Voltigeur(line=l,        row=r - 1,      batch=self.batch),
            Voltigeur(line=l + 1,    row=r,          batch=self.batch),
            Voltigeur(line=l + 1,    row=r - 1,      batch=self.batch),
            Voltigeur(line=l + 1,    row=r + 1,      batch=self.batch),
            Voltigeur(line=l - 1,    row=r,          batch=self.batch),
            Voltigeur(line=l - 1,    row=r - 1,      batch=self.batch),
            Voltigeur(line=l - 1,    row=r + 1,      batch=self.batch),


        ]
        for unit in units :
            self.add_unit(unit)
        bataillon = Bataillon(units,self.grid)
        for unit in units:
            unit.set_bataillon(len(self.bataillons))
        self.bataillons.append(bataillon)


        ### 2eme bataillon :

        l = 10
        r = 10
        units = [
            OldGuard(line=l,            row=r,          batch=self.batch),
            OldGuard(line=l,            row=r + 1,      batch=self.batch),
            OldGuard(line=l,            row=r - 1,      batch=self.batch),
            OldGuard(line=l + 1,        row=r,          batch=self.batch),
            OldGuard(line=l + 1,        row=r - 1,      batch=self.batch),
            OldGuard(line=l + 1,        row=r + 1,      batch=self.batch),
            OldGuard(line=l - 1,        row=r,          batch=self.batch),
            OldGuard(line=l - 1,        row=r - 1,      batch=self.batch),
            OldGuard(line=l - 1,        row=r + 1,      batch=self.batch),

        ]
        for unit in units:
            self.add_unit(unit)
        bataillon = Bataillon(units, self.grid)
        for unit in units:
            unit.set_bataillon(len(self.bataillons))
        self.bataillons.append(bataillon)

        ### 3eme bataillon :

        l = 1
        r = 1
        units = [
            Canon(line=l, row=r, batch=self.batch),

        ]
        for unit in units:
            self.add_unit(unit)
        bataillon = Bataillon(units, self.grid)
        for unit in units:
            unit.set_bataillon(len(self.bataillons))
        self.bataillons.append(bataillon)


    def handle_key(self,key):
        if key == pyglet.window.key.B:
            if self.clicked_bataillon:
                self.clicked_bataillon.set_bayonet()

    def main(self):
        self.init_bandeau()
        for bat in self.bataillons :
            bat.move_bataillon()
        if self.shoot :
            self.bataillon.shoot()


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
