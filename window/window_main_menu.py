import pyglet
from window.input_handler import input_handler
from units.oldguard import OldGuard
from units.voltigeur import Voltigeur
from pyglet import font
from window.buttons import Button , UnitButton
from window.window import Window
from game import Game

from units.bataillon import Bataillon
pyglet.resource.path = ['ressources']
pyglet.resource.reindex()
font.add_file('ressources/napo.ttf')
napo_font = font.load('ressources/napo.ttf', 16)

def play_music():
    music = pyglet.resource.media('sounds/misc/main_menu.mp3',streaming=False)
    return music


class Window_main_menu(pyglet.window.Window):
    def __init__(self):
        super(Window_main_menu, self).__init__()
        Window_main_menu.set_caption(self, caption="Napoléon ")
        Window_main_menu.set_fullscreen(self, fullscreen=True)
        self.batch = pyglet.graphics.Batch()

        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.middle_ground = pyglet.graphics.OrderedGroup(1)
        self.fore_ground = pyglet.graphics.OrderedGroup(2)
        background_image = pyglet.resource.image('imgs/window/main_menu2.jpg')
        background_image.width = 1900
        self.background = pyglet.sprite.Sprite(background_image,
                                               batch=self.batch, group=self.background_group)


        ## TITLE

        title_button = pyglet.shapes.Rectangle(7 * self.height // 9, 4.1 * self.width // 9, 800, 120,
                                               color=(74, 52, 168),
                                               batch=self.batch, group=self.middle_ground)

        title_button.opacity = 20
        label = pyglet.text.Label('Napoleon Campaign Defense',
                                  font_name='Napoleon Inline',
                                  font_size=72,
                                  x=1.1 * title_button.x, y=1.06 * title_button.y,
                                  batch=self.batch, group=self.fore_ground,
                                  color=(255, 215, 0, 255))
        self.title = (title_button, label)


        self.buttons = []

        self.generate_main()
        self.player = pyglet.media.Player()
        self.player.queue(play_music())
        self.player.play()
    def generate_main(self):
        for but in self.buttons:
            but.delete()
        self.buttons.clear()

        # Escarmouche:

        background_image = pyglet.resource.image('imgs/window/main_menu2.jpg')
        background_image.width = 1900
        self.background = pyglet.sprite.Sprite(background_image,
                                               batch=self.batch, group=self.background_group)

        launch_game_button = Button('Escarmouche',self.height//4, self.width//4, 400, 80,'Escarmouche',self.batch,self.middle_ground,(0, 0, 0))

        self.buttons.append(launch_game_button)
        options_button =  Button('Options',self.height//8, self.width//8, 300, 80,'Options',self.batch,self.middle_ground,(0, 0, 0))
        self.buttons.append(options_button)



        self.units = []
        self.bataillons = []

        ## Title



        self.menu = "main"


    def handle_key(self, key):
        if key == pyglet.window.key.ESCAPE:
            self.close()



    def handle_right(self,x,y):
        if self.menu == "main" :
            for buton in self.buttons:
                if buton.name=="Escarmouche" and buton.is_pressed(x,y):
                    self.menu = "bataillons"
                    self.generate_menu_bataillons()
                    return

        if self.menu =="bataillons":
            for button in self.buttons :
                if button.name =="Commencer" and button.is_pressed(x,y):

                            bataillon =Bataillon(self.units)
                            self.bataillons.append(bataillon)
                            game = Game()
                            window = Window(game,self.bataillons)
                            input_handler(window)
                            # self.music.get_next_video_timestamp()
                            self.close()
                            self.player.pause()
                            pyglet.app.run()

                if button.name == "Retour" and button.is_pressed(x,y):
                    self.menu = "main"
                    self.generate_main()
                    return

                ### ADD UNIT TO BATAILLON :
                if button.name == "OldGuard" and button.is_pressed(x, y):
                    unit = OldGuard(line=10,            row=5,          batch= pyglet.graphics.Batch())
                    self.units.append(unit)
                    unit.set_bataillon(len(self.bataillons))
                    return


                if button.name == "Voltigeur" and button.is_pressed(x, y):
                    unit = Voltigeur(line=11, row=6, batch=pyglet.graphics.Batch())
                    self.units.append(unit)
                    unit.set_bataillon(len(self.bataillons))
                    return


    def handle_left(self,x,y):
        return

    def on_mouse_motion(self,x,y,dx,dy):
        if self.menu =="main" or self.menu=="bataillons":
            for button in self.buttons :
                try :
                    button.is_hovered(x,y)
                except:
                    pass
    def on_draw(self):
        self.clear()
        if self.menu =="main":
            self.batch.draw()
        if self.menu =="bataillons":
            self.batch.draw()


    def generate_menu_bataillons(self):
        for but in self.buttons:
            but.delete()
        self.buttons.clear()
        background_image = pyglet.resource.image('imgs/window/bataillons_menu.jpg')
        background_image.width = 1900
        self.background = pyglet.sprite.Sprite(background_image,
                                               batch=self.batch, group=self.background_group)

        launch_game_button = Button('Retour', self.height // 4, self.width // 4, 400, 80, 'Retour',
                                    self.batch, self.middle_ground, (0, 0, 0))

        self.buttons.append(launch_game_button)

        ### Création des bataillons à selectionner
        self.generate_bataillons()
        LaunchGame_button = Button('Commencer', self.height // 8, self.width // 8, 300, 80, 'Commencer', self.batch,
                                   self.middle_ground, (0, 0, 0))
        self.buttons.append(LaunchGame_button)


        ## CREATE BATAILLONS MENU :
        for i in range(9):

            LaunchGame_button = Button('empty_case',85*i + 0.7* self.height , 0.3*self.width , 80, 80, '', self.batch,
                                       self.middle_ground, (0, 0, 0))
            self.buttons.append(LaunchGame_button)
        # bataillon 1 :

        self.init_bataillons()


    def init_bataillons(self):

        self.bataillons = []


    def generate_bataillons(self):

     unit = UnitButton('OldGuard', 0.7*self.height , 0.4*self.width , 300, 80, 'OlGuard', self.batch,
                               self.middle_ground, (0, 0, 0))
     self.buttons.append(unit)

     unit = UnitButton('Voltigeur', 0.9 * self.height, 0.4 * self.width, 300, 80, 'Voltigeur', self.batch,
                       self.middle_ground, (0, 0, 0))
     self.buttons.append(unit)
