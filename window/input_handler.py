from pyglet.window import key
from pyglet.window import mouse
from pyglet.clock import Clock
from units.oldguard import OldGuard
from pyglet import clock

def motion_handler(dt,window):
    @window.event
    def on_mouse_motion(x, y, dx, dy):
        print("CALLED")
        window.get_element(x,y,action="HOVER")


def input_handler(window):
    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.A:
            window.label.text = str(window.camera.x)
        elif symbol == key.ENTER:
            window.set_fullscreen()
            print('The enter key was pressed.')
        # Camera Handler
        if symbol == key.LEFT:
            window.camera.move_left()
        if symbol == key.RIGHT:
            window.camera.move_right()





    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
            window.get_element(x,y,action="CLICK")
            # window.move=True
            # window.shoot = False
        if button == mouse.RIGHT:
            window.handle_left(x,y)
            #window.shoot = True
            #window.move = False
