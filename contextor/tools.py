from typing import Callable, Final, TypeVar
from collections import defaultdict
import queue

from pyglet import clock
from loguru import logger

from .structures import Event

EventHandlerT = TypeVar("EventHandlerT", bound=Callable[[], None])


class EventManager:
    MAX_EVENTS_PER_TICK: Final[int] = 4

    event_queue: queue.Queue[Event]
    handlers: dict[Event, list[EventHandlerT]]

    def __init__(self) -> None:
        self.event_queue = queue.Queue()
        self.handlers = defaultdict(list)

    @property
    def queue(self) -> queue.Queue[Event]:
        return self.event_queue

    @logger.catch(level="debug")
    def dispatch(self, event: Event):
        self.event_queue.put_nowait(event)

    def on(self, event: Event) -> Callable[[EventHandlerT], EventHandlerT]:
        def decorator(func: EventHandlerT) -> EventHandlerT:
            self.handlers[event].append(func)
            return func
        return decorator

    @logger.catch()
    def daemon(self, delta: float):
        for _ in range(self.MAX_EVENTS_PER_TICK):
            try:
                event = self.event_queue.get_nowait()
            except queue.Empty:
                return

            handlers = self.handlers.get(event)
            if handlers is None:
                return

            for f in handlers:
                f()

    def install_daemon(self, interval: float | int = 0.1):
        clock.schedule_interval(self.daemon, interval=interval)


event_mngr = EventManager()
