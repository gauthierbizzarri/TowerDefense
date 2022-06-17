import pyglet
from window.input_handler import input_handler
pyglet.resource.path = ['ressources']
pyglet.resource.reindex()


from pyglet import font
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


        self.buttons = []

        self.labels = []

        self.init_butons()
        self.player = pyglet.media.Player()
        self.player.queue(play_music())
        self.player.play()
    def init_butons(self):


        # Escarmouche:
        launch_game_button = pyglet.shapes.Rectangle(self.height//4, self.width//4, 400, 80, color=(0, 0, 0), batch=self.batch, group = self.middle_ground)
        launch_game_button.opacity = 180
        label = pyglet.text.Label('Escarmouche',
                                  font_name='Napoleon Inline',
                                  font_size=36,
                                  x=1.1*launch_game_button.x, y=1.06*launch_game_button.y,
                                   batch=self.batch , group = self.fore_ground)
        self.labels.append(label)
        self.buttons.append(launch_game_button)

        # Options:
        options_button = pyglet.shapes.Rectangle(self.height // 8, self.width // 8, 300, 80, color=(0, 0, 0),
                                                     batch=self.batch, group=self.middle_ground)
        options_button.opacity = 180
        label_options = pyglet.text.Label('Options',
                                  font_name='Napoleon Inline',
                                  font_size=36,
                                  x=1.1 * options_button.x, y=1.06 * options_button.y,
                                  batch=self.batch, group=self.fore_ground)
        self.labels.append(label_options)
        self.buttons.append(options_button)

        ## Title

        title_button = pyglet.shapes.Rectangle(3*self.height //9  , 3.8*self.width//9 , 800, 120, color=(74,52,168),
                                               batch=self.batch, group=self.middle_ground)
        title_button.opacity = 40
        label = pyglet.text.Label('Napoleon Campaign Defense',
                                  font_name='Napoleon Inline',
                                  font_size=72,
                                  x=1.1*title_button.x, y=1.06 * title_button.y,
                                  batch=self.batch, group=self.fore_ground,
                                  color=(255, 215, 0, 255))
        self.labels.append(label)
        self.buttons.append(title_button)

    def handle_key(self, key):
        if key == pyglet.window.key.ESCAPE:
            self.close()



    def handle_right(self,x,y):
        from window.window import Window
        from game import Game
        if x <= self.buttons[0].x + self.buttons[0].width and x >= self.buttons[0].x:
            if y <= self.buttons[0].y + self.buttons[0].height and y >= self.buttons[0].y:
                game = Game()
                window = Window(game)
                input_handler(window)
                # self.music.get_next_video_timestamp()
                self.close()
                self.player.pause()
                pyglet.app.run()
    def handle_left(self,x,y):
        return

    def on_mouse_motion(self,x,y,dx,dy):
        for button in self.buttons :
            if x <= button.x + button.width and x >= button.x:
                if y <= button.y + button.height and y >= button.y:
                    if button.color == (74,52,168) : return
                    button.color =(50, 50, 50)

            else :
                if button.color == (74,52,168): return
                button.color = (0, 0, 0)
    def on_draw(self):
        self.clear()
        for lab in self.labels :
            lab.draw()
        self.batch.draw()
