from pyglet.window import key
from pyglet.window import mouse
from pyglet.clock import Clock
from units.oldguard import OldGuard
from pyglet import clock

def motion_handler(dt,window):
    @window.event
    def on_mouse_motion(x, y, dx, dy):
        pass
        # window.get_element(x,y,action="HOVER")


def input_handler(window):
    @window.event
    def on_key_press(symbol, modifiers):
        window.handle_key(symbol)





    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
            window.handle_right(x,y)
        if button == mouse.RIGHT:
            window.handle_left(x,y)
