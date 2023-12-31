import numpy as np

from .structures import Event
from .binds import mouse_ctrl
from . import tools, layout


# TODO: rework
# @layout.window.event("on_deactivate")
def on_unfocus():
    hide_window()


@tools.event_mngr.on(Event.HIDE)
def hide_window():
    if not layout.window.visible:
        layout.window.set_location(
            *np.clip(
                mouse_ctrl.position - np.array(layout.window.size) // 2,
                (0, 0),
                layout.screen_size - layout.window.size
            )
        )
    layout.window.set_visible(not layout.window.visible)
