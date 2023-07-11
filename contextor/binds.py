from pynput import keyboard, mouse

from .structures import Event
from . import tools


def kb_press(key: keyboard.Key | keyboard.KeyCode | None):
    if key == keyboard.KeyCode(char="x"):
        tools.event_mngr.dispatch(Event.HIDE)


def kb_release(key: keyboard.Key | keyboard.KeyCode | None):
    return


def start():
    kb_listner.start()


mouse_ctrl = mouse.Controller()
kb_listner = keyboard.Listener(on_press=kb_press, on_release=kb_release)
