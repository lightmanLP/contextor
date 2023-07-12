from pynput import keyboard as kb, mouse

from .structures import Event
from . import tools


def kb_press(key: kb.Key | kb.KeyCode | None):
    ### DEBUG
    if key == kb.KeyCode(char="-"):
        tools.event_mngr.dispatch(3)
    elif key == kb.KeyCode(char="="):
        tools.event_mngr.dispatch(2)
    ###


def kb_release(key: kb.Key | kb.KeyCode | None):
    if key == kb.KeyCode(char="x"):
        tools.event_mngr.dispatch(Event.HIDE)


def start():
    kb_listner.start()


mouse_ctrl = mouse.Controller()
kb_listner = kb.Listener(on_press=kb_press, on_release=kb_release)
