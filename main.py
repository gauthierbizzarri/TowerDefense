import pyglet
from window.input_handler import input_handler, motion_handler
from window.window import  Window
from pyglet import clock
from game import Game

pyglet.resource.path = ['ressources']
pyglet.resource.reindex()







def play_music():
    # streaming = False for longer tracks
    music = pyglet.resource.media('sounds/misc/austerlitzmp3', streaming=True)
    # music.play()
    # vive_empereur = pyglet.resource.media('viveempereur.mp3', streaming=True)
    music.play()



if __name__ == '__main__':
    game = Game()
    window = Window(game)
    image = pyglet.image.load('ressources/imgs/misc/cursor.png')
    image.anchor_y = +10
    cursor = pyglet.window.ImageMouseCursor(image, 16, 8)
    window.set_mouse_cursor(cursor)
    play_music()
    event_loop = pyglet.app.EventLoop()
    input_handler(window)
    # clock.schedule_once(motion_handler, 5,window)
    pyglet.app.run()
    # window.update()
    # play_music()