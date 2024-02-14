from typing import Callable, Final, TypeVar, Iterable, TypeAlias, Any
from typing_extensions import Self
from collections import defaultdict
import functools
import queue

from pyglet import clock
from loguru import logger

from .structures import Event

EventSpecT: TypeAlias = tuple[Event, tuple, dict[str, Any]]
EventHandlerT = TypeVar("EventHandlerT", bound=Callable)


class ObjectStash:
    objs: list[Any]

    def __init__(self) -> None:
        self.objs = list()

    def __iadd__(self, obj: Any) -> Self:
        self.objs.append(obj)
        return self

    def __imul__(self, objs: Iterable[Any]) -> Self:
        self.objs.extend(objs)
        return self


class EventManager:
    MAX_EVENTS_PER_TICK: Final[int] = 4

    event_queue: queue.Queue[EventSpecT]
    handlers: dict[Event, list[EventHandlerT]]

    def __init__(self) -> None:
        self.event_queue = queue.Queue()
        self.handlers = defaultdict(list)

    @property
    def queue(self) -> queue.Queue[EventSpecT]:
        return self.event_queue

    @logger.catch(level="debug")
    def dispatch(self, event: Event, *args, **kwargs):
        self.event_queue.put_nowait((event, args, kwargs))

    def dispatcher(self, event: Event) -> functools.partial["dispatch"]:
        return functools.partial(self.dispatch, event)

    def on(self, event: Event) -> Callable[[EventHandlerT], EventHandlerT]:
        def decorator(func: EventHandlerT) -> EventHandlerT:
            self.handlers[event].append(func)
            return func
        return decorator

    @logger.catch()
    def daemon(self, delta: float):
        for _ in range(self.MAX_EVENTS_PER_TICK):
            try:
                event, args, kwargs = self.event_queue.get_nowait()
            except queue.Empty:
                return

            handlers = self.handlers.get(event)
            if not handlers:
                return

            for f in handlers:
                f(*args, **kwargs)

    def install_daemon(self, interval: float | int = 0.1):
        clock.schedule_interval(self.daemon, interval=interval)


event_mngr = EventManager()
