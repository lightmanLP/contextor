from typing import Final
from pathlib import Path

from pyglet.window import Window
from pyglet import gl, graphics, shapes, canvas, compat_platform
import numpy as np
from ruamel.yaml import YAML

from .structures import Color

CIRCLE_RADIUS: Final[int] = 18
MAX_LAYERS: Final[int] = 3
LAYOUT_PATH: Final[Path] = Path.cwd() / "layout.yml"


yaml = YAML(typ="safe", pure=True)

# sorted(size: points)
layout: dict[int, list[tuple[int, int]]]
with open(LAYOUT_PATH, encoding="UTF-8") as file:
    layout = yaml.load(file)
    assert isinstance(layout, dict)
    assert len(layout) > 0
    layout = dict(sorted(layout.items(), key=lambda x: x[0]))

config = gl.Config(sample_buffers=1, samples=4)
display = canvas.Display()
screen: canvas.Screen = display.get_default_screen()
screen_size = np.array((screen.width, screen.height))

win_size = int((CIRCLE_RADIUS * 2) * ((MAX_LAYERS * 2 + 1) * 1.5))
window = Window(
    win_size, win_size,
    style=Window.WINDOW_STYLE_OVERLAY,
    config=config,
    visible=False
)
center = np.array(window.size) // 2

# no taskbar icon patch
if compat_platform in ('cygwin', 'win32'):
    from pyglet.libs.win32.constants import WS_EX_TOOLWINDOW, GWL_EXSTYLE
    from pyglet.libs.win32 import _user32
    window._ex_ws_style |= WS_EX_TOOLWINDOW
    _user32.SetWindowLongW(window._hwnd, GWL_EXSTYLE, window._ex_ws_style)


### DEBUG
count = 0
from .tools import event_mngr
@event_mngr.on(2)
def inc():
    global count
    count += 1
@event_mngr.on(3)
def dec():
    global count
    count -= 1
###


@window.event
def on_draw():
    window.clear()
    batch = graphics.Batch()

    if count == 0:
        main_circle = shapes.Circle(
            *center,
            CIRCLE_RADIUS,
            color=Color.RED.rgba,
            batch=batch
        )

    else:
        for max_count, points in layout.items():
            if count <= max_count:
                break
        circles = [
            shapes.Circle(
                *(center + point),
                CIRCLE_RADIUS,
                color=Color.PURPLE.rgba,
                batch=batch
            )
            for point in points[:count]
        ]

    batch.draw()
