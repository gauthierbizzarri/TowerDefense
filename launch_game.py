import pyglet
from window.input_handler import input_handler
from window.window import  Window
from pyglet import clock
from game import Game
from window.window_main_menu import Window_main_menu
pyglet.resource.path = ['ressources']
pyglet.resource.reindex()









if __name__ == '__main__':
    main_window = Window_main_menu()
    input_handler(main_window)
    pyglet.app.run()