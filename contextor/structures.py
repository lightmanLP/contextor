from enum import IntEnum
import functools


class Event(IntEnum):
    HIDE = 1


class Color(IntEnum):
    PURPLE = 0x550055A0

    @functools.cached_property
    def rgba(self) -> tuple[int, int, int, int]:
        value = self.value
        color = list()
        for _ in range(4):
            value, cur = divmod(value, 0xFF)
            color.append(cur)
        return tuple(reversed(color))

    @functools.cache
    def rgbac(self, alpha: int):
        return (*self.rgba[:-1], alpha)
