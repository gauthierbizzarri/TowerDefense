import pyglet
from window.input_handler import input_handler
from window.window import  Window
from pyglet import clock
from game import Game

pyglet.resource.path = ['ressources']
pyglet.resource.reindex()









if __name__ == '__main__':
    game = Game()
    window = Window(game)

    # event_loop = pyglet.app.EventLoop()
    input_handler(window)
    pyglet.app.run()