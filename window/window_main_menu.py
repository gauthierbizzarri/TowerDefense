import pyglet
from window.input_handler import input_handler
pyglet.resource.path = ['ressources']
pyglet.resource.reindex()


from pyglet import font
font.add_file('ressources/napo.ttf')
napo_font = font.load('ressources/napo.ttf', 16)

class Window_main_menu(pyglet.window.Window):
    def __init__(self):
        super(Window_main_menu, self).__init__()
        Window_main_menu.set_caption(self, caption="Napoléon ")
        Window_main_menu.set_fullscreen(self, fullscreen=True)
        self.batch = pyglet.graphics.Batch()

        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.middle_ground = pyglet.graphics.OrderedGroup(1)
        self.fore_ground = pyglet.graphics.OrderedGroup(2)
        background_image = pyglet.resource.image('imgs/window/main_menu.jpg')
        background_image.width = 1900
        self.background = pyglet.sprite.Sprite(background_image,
                                               batch=self.batch, group=self.background_group)


        self.buttons = []

        self.labels = []

        self.init_butons()


    def init_butons(self):
        # Create game :
        launch_game_button = pyglet.shapes.Rectangle(self.height//4, self.width//4, 400, 80, color=(0, 0, 0), batch=self.batch, group = self.middle_ground)
        launch_game_button.opacity = 125
        label = pyglet.text.Label('Escarmouche',
                                  font_name='Napoleon Inline',
                                  font_size=36,
                                  x=1.1*launch_game_button.x, y=1.06*launch_game_button.y,
                                   batch=self.batch , group = self.fore_ground)
        self.labels.append(label)
        self.buttons.append(launch_game_button)

    def handle_key(self, key):
        if key == pyglet.window.key.ESCAPE:
            self.close()



    def handle_right(self,x,y):
        pass
    def handle_left(self,x,y):
        from window.window import Window
        from game import Game
        game = Game()
        window = Window(game)
        input_handler(window)

        self.close()
        pyglet.app.run()


    def on_draw(self):
        self.clear()
        for lab in self.labels :
            lab.draw()
        self.batch.draw()
