from typing import Iterator, Literal
from collections import defaultdict
from pathlib import Path
import functools
import math

import numpy as np
from ruamel.yaml import YAML, representer

from contextor import layout

LAYOUT_PATH = Path.cwd() / "layout.yml"


class NonAliasingRepresenter(representer.RoundTripRepresenter):
    def ignore_aliases(self, *args) -> Literal[True]:
        return True


yaml = YAML(typ="safe", pure=True)
yaml.Representer = NonAliasingRepresenter
yaml.indent(mapping=2, sequence=4, offset=2)

r = layout.CIRCLE_RADIUS + 2
base_r_big = int(r * 2)
r_step = r * 2


# TODO: replace with np.cos, np.sin
def calc_coords(r_big: int, count: int) -> Iterator[tuple[int, int]]:
    offset = r_big - r
    for i in range(count):
        cur = (2 * math.pi) * i / count
        coords = (
            offset * math.cos(cur),
            offset * math.sin(cur)
        )
        yield tuple(map(int, coords))


@functools.cache
def calc_count(r_big: int) -> int:
    ratio = r / (r_big - r)
    return int(math.pi / abs(math.asin(ratio)))


def run(
    max_first_layer_count: int | None = None,
    bottom_line: int | None = None
):
    max_first_layer_count = max_first_layer_count or 8
    bottom_line = bottom_line or 3

    r_big = base_r_big
    count_to_radius = dict()
    while (count := calc_count(r_big)) <= max_first_layer_count:
        count_to_radius[count] = r_big
        r_big += 1

    data = defaultdict(list)
    for count, r_big in reversed(count_to_radius.items()):
        data[count].extend(calc_coords(r_big, count))
        if count < bottom_line:
            continue
        for layer in range(1, layout.MAX_LAYERS):
            r_big += r_step
            local_count = calc_count(r_big)
            data[count + local_count].extend(data[count])
            count += local_count
            data[count].extend(calc_coords(r_big, local_count))

    data = dict(sorted(data.items(), key=lambda x: x[0]))
    with open(LAYOUT_PATH, "w", encoding="UTF-8") as file:
        yaml.dump(data, file)
