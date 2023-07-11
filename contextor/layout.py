from pyglet.window import Window
from pyglet import gl, graphics, shapes, canvas
import numpy as np

from .structures import Color


config = gl.Config(sample_buffers=1, samples=4)
batch = graphics.Batch()
display = canvas.Display()
screen: canvas.Screen = display.get_default_screen()
screen_size = np.array((screen.width, screen.height))

window = Window(
    width=200, height=200,
    style=Window.WINDOW_STYLE_OVERLAY,
    config=config,
    visible=False
)
circle = shapes.Circle(
    *(np.array(window.size) // 2),
    20,
    color=Color.PURPLE.rgba,
    batch=batch
)
