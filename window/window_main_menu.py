import pyglet
from window.input_handler import input_handler , motion_handler
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
        try :
            if self.coin_img :
                self.coin_img.delete()
            if self.coin_text:
                self.coin_text.delete()
        except:
            pass

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

        self.selected_unit = False
        self.menu = "main"

        self.budget = 500
        self.coin_text = None

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


                            game = Game()
                            window = Window(game,self.bataillons)
                            input_handler(window)
                            motion_handler(window)
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
                    self.selected_unit = "OldGuard"
                    return
                if button.name == "Voltigeur" and button.is_pressed(x, y):
                    self.selected_unit = "Voltigeur"
                    return

                if button.name == "empty_case" and button.is_pressed(x, y) and self.selected_unit :
                    if self.selected_unit =="OldGuard":
                        if self.budget>=200:
                            units = []
                            for but in self.buttons:
                                if but.name =="empty_case" and but.bataillon == button.bataillon:
                                    unit = OldGuard(line=but.line, row=but.row, batch=pyglet.graphics.Batch())
                                    units.append(unit)
                                    self.units.append(unit)
                                    unit.set_bataillon(len(self.bataillons))
                                    but.name=="OldGuard"
                                    but.set_img("OldGuard")
                                    self.coin_text.text = str(self.budget)
                            bataillon = Bataillon(units)
                            self.bataillons.append(bataillon)
                            self.budget = self.budget - 200
                            return
                    if self.selected_unit =="Voltigeur":
                        if self.budget >= 100:
                            units = []
                            for but in self.buttons:
                                if but.name == "empty_case" and but.bataillon == button.bataillon:
                                    unit = Voltigeur(line=but.line, row=but.row, batch=pyglet.graphics.Batch())
                                    units.append(unit)
                                    self.units.append(unit)
                                    unit.set_bataillon(len(self.bataillons))
                                    but.name == "Voltigeur"
                                    but.set_img("Voltigeur")
                                    self.coin_text.text = str(self.budget)

                            bataillon = Bataillon(units)
                            self.bataillons.append(bataillon)
                            self.budget = self.budget - 100
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

        coin_img  = pyglet.resource.image('imgs/misc/coins.png')
        coin_img.width = 50
        coin_img.height = 50
        x = 4/15 * self.width
        y = 7 / 10 * self.height
        self.coin_img = pyglet.sprite.Sprite(coin_img ,x =x , y=y  ,
                                               batch=self.batch, group=self.fore_ground)
        self.coin_text = pyglet.text.Label(str(self.budget),
                                  font_name='Napoleon Inline',
                                  font_size=36,
                                  x=x + 80, y=y,
                                  batch=self.batch, group=pyglet.graphics.OrderedGroup(2))

        launch_game_button = Button('Retour', self.height // 4, self.width // 4, 400, 80, 'Retour',
                                    self.batch, self.middle_ground, (0, 0, 0))

        self.buttons.append(launch_game_button)

        ### Création des bataillons à selectionner
        self.generate_bataillons()
        LaunchGame_button = Button('Commencer', self.height // 8, self.width // 8, 300, 80, 'Commencer', self.batch,
                                   self.middle_ground, (0, 0, 0))
        self.buttons.append(LaunchGame_button)


        ## BATAILLON 1 / CREATE BATAILLONS MENU :
        for col in range(4):
            for lin in range(3):

                LaunchGame_button = Button('empty_case',55*lin + 0.7* self.height , 0.35*self.width - col*55 , 50, 50, '', self.batch,
                                           self.middle_ground, (0, 0, 0),col,lin, 0)
                self.buttons.append(LaunchGame_button)
                ## BATAILLON 2 / CREATE BATAILLONS MENU :
        for col in range(5,9):
            for lin in range(3):
                LaunchGame_button = Button('empty_case', 55 * lin + 0.7 * self.height, 0.35 * self.width - col * 55 ,
                                           50, 50, '', self.batch,
                                           self.middle_ground, (0, 0, 0), col, lin, 1)
                self.buttons.append(LaunchGame_button)

        self.init_bataillons()


    def init_bataillons(self):

        self.bataillons = []


    def generate_bataillons(self):

     unit = UnitButton('OldGuard', 0.7*self.height , 0.4*self.width , 300, 80, '200', self.batch,
                               self.middle_ground, (0, 0, 0))
     self.buttons.append(unit)

     unit = UnitButton('Voltigeur', 0.9 * self.height, 0.4 * self.width, 300, 80, '100', self.batch,
                       self.middle_ground, (0, 0, 0))
     self.buttons.append(unit)
