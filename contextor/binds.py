from pynput import keyboard as kb, mouse
import numpy as np

from .structures import Event
from . import tools, layout


def kb_press(key: kb.Key | kb.KeyCode | None):
    if key is None:
        return
    match getattr(key, "char", None):
        ### DEBUG
        case "-":
            tools.event_mngr.dispatch(98)
        case "=":
            tools.event_mngr.dispatch(99)
        ###


def kb_release(key: kb.Key | kb.KeyCode | None):
    if key is None:
        return
    match getattr(key, "char", None):
        case "x":
            tools.event_mngr.dispatch(Event.HIDE)


def mouse_click(x: int, y: int, button: mouse.Button, pressed: bool):
    if not layout.window.visible:
        return
    coords = np.array((x, y)) - layout.window.get_location()
    if ((coords >= (0, 0)) & (coords <= layout.window.size)).all():
        tools.event_mngr.dispatch(Event.CLICK, coords)
    else:
        tools.event_mngr.dispatch(Event.HIDE)


def start():
    kb_listner.start()
    mouse_listener.start()


mouse_ctrl = mouse.Controller()
kb_listner = kb.Listener(on_press=kb_press, on_release=kb_release)
mouse_listener = mouse.Listener(on_click=mouse_click)
