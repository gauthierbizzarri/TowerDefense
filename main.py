import pyglet
from window.input_handler import input_handler
from window.window import  Window
from game import Game
pyglet.resource.path = ['ressources']
pyglet.resource.reindex()







def play_music():
    # streaming = False for longer tracks
    music = pyglet.resource.media('music.mp3', streaming=True)
    # music.play()
    vive_empereur = pyglet.resource.media('viveempereur.mp3', streaming=True)
    vive_empereur.play()



if __name__ == '__main__':
    game = Game()
    window = Window(game)
    input_handler(window)
    pyglet.app.run()
    # window.update()
    # play_music()