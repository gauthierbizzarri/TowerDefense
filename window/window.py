import pyglet
from units.voltigeur import Voltigeur
from config.settings import *
from terrain.grid import Grid
from terrain.grid import get_line_row
from units.bataillon import Bataillon
from window.camera import Camera

image= pyglet.resource.image('ressources/imgs/bataillon.png')


def play_music():
    music = pyglet.resource.media('sounds/misc/austerlitz.mp3',streaming=False)
    return music





def img_bataillon():
    frames = []
    img = pyglet.resource.image('ressources/imgs/bataillon.png')
    frame = pyglet.image.AnimationFrame(img, duration=0.5)
    frames.append(frame)

    ani = pyglet.image.Animation(frames=frames)
    return ani



class Window(pyglet.window.Window):

    def __init__(self, game, bataillons):
        super(Window, self).__init__()
        Window.set_caption(self, caption="Napoléon ")
        Window.set_fullscreen(self, fullscreen=True)


        self.batch = pyglet.graphics.Batch()
        self.game = game

        self.camera = Camera()


        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.middleground_group = pyglet.graphics.OrderedGroup(1)
        self.foreground_group = pyglet.graphics.OrderedGroup(2)


        self.grid = Grid(batch=self.batch,group=self.middleground_group)

        self.bandeau = []

        self.clicked_unit = None
        background_image = pyglet.resource.image('imgs/window/back.jpg')
        background_image.width = 4000
        self.background = pyglet.sprite.Sprite(background_image,
                                               batch=self.batch, group=self.background_group)

        self.decor = self.grid.create_decor(self.foreground_group)


        self.move = False
        self.shoot = False


        self.clicked_bataillon = None


        self.bataillons = []


        self.init_armee(bataillons)


        self.init_bandeau()
        self.grid.update()

        self.player = pyglet.media.Player()
        self.player.queue(play_music())
        self.player.play()






    def init_bandeau(self):
        return
        separator = 0
        for element in self.bataillons:
            self.bandeau.append(
               #  (shapes.BorderedRectangle(LEFT_BORDER + separator, 0,100  ,110,  border=3, color=(0, 0, 0),
                #                          border_color=(0, 255, 0), batch=self.batch, group=self.foreground_group),

                 pyglet.sprite.Sprite(img=img_bataillon(), x=LEFT_BORDER + separator , y=0,
                                      batch=self.batch, group=self.foreground_group))
            separator +=BLOCKSIZE+100


    def get_element(self,x,y,action):
        if self.clicked_bataillon is not None:
            for unit in self.clicked_bataillon.units :
                unit.is_selected = False
        element = self.grid.get_element(x,y,action)[0]
        if action =="CLICK":
            if element is not None :
                self.clicked_unit = element
                self.clicked_bataillon = self.bataillons[self.clicked_unit.bataillon]
                for unit in self.clicked_bataillon.units:
                    unit.is_selected = True

    def handle_right(self,x,y):
        self.get_element(x,y,action="CLICK")
    def handle_left(self,x,y):
        content = self.grid.get_element(x, y)[1]

        if self.clicked_unit :
            ### CHECK FREE :
            if content == "NONE":
                # self.grid.draw_bataillon_selected(self.clicked_bataillon)
                self.clicked_bataillon.add_path(self.grid.get_matrix_for_path(),get_line_row(x,y)[0],get_line_row(x,y)[1],self.clicked_unit)
                self.grid.set_move_tile(get_line_row(x,y)[0],get_line_row(x,y)[1])
                self.grid.update()
            if content == "UNIT":
               ###### SHOOT
                target = self.bataillons[self.grid.get_element(x, y)[0].bataillon]
                # self.grid.set_move_tile(get_line_row(x, y)[0], get_line_row(x, y)[1])
                self.clicked_bataillon.shoot(target)

    def init_armee(self,bataillons ):
        for bat in bataillons:
            for unit in bat.units :
                self.add_unit(unit)
            bat.set_batch(self.batch)
            bat.set_grid(self.grid)
            self.bataillons.append(bat)
            bat.create_path_spawn(self.grid.get_matrix_for_path())

    def update_camera(self,camera):
        ### Update unit on camera :

        self.background.x = self.background.x + camera.x
        self.background.y = self.background.y + camera.y


    def handle_key(self,key):
        if key == pyglet.window.key.B:
            if self.clicked_bataillon:
                self.clicked_bataillon.set_bayonet()

        if key == pyglet.window.key.A :
            self.camera.move_left()

        if key == pyglet.window.key.Z:
            self.camera.move_right()

    def main(self):


        # get_transform
        for bat in self.bataillons :
            bat.main()
            for unit in bat.units :
                if unit.health <= 0 :
                    bat.units.remove(unit)
                    self.grid.unset_unit(unit)

            bat.move_bataillon()
            bat.play_effect()



        if self.shoot :
            self.bataillon.shoot()


    def add_unit(self, unit):
        self.game.add_unit(unit)
        self.grid.set_unit(unit)




    def on_draw(self):
        self.clear()
        self.main()
        self.batch.draw()
