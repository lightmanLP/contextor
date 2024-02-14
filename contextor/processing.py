import numpy as np

from .structures import Event
from .binds import mouse_ctrl
from . import tools, layout


@tools.event_mngr.on(Event.HIDE)
def hide_window():
    new_state = not layout.window.visible
    if new_state:
        layout.window.set_location(
            *np.clip(
                mouse_ctrl.position - np.array(layout.window.size) // 2,
                (0, 0),
                layout.screen_size - layout.window.size
            )
        )
    layout.window.set_visible(new_state)
    if new_state:
        layout.window.activate()
