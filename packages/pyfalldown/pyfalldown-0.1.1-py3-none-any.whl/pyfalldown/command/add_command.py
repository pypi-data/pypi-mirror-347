import random

from pyfalldown.state import Platform, State

from .command import Command


def add(
    state: State,
    half_height: int,
    min_half_width: int,
    max_half_width: int,
    max_x: int,
    vertical_gap_to_last: int,
    add_collectible_func: Command,
    collectible_prob: float = 0.7,
) -> State:
    if len(state.platforms) >= 10:
        return state
    half_width = random.randint(min_half_width, max_half_width)
    x = random.randint(half_width, max_x - half_width)
    y = 0 if not state.platforms else state.platforms[-1].y
    state.platforms[:] = [*state.platforms, Platform(x, y + vertical_gap_to_last, half_width, half_height)]
    if random.random() < collectible_prob:
        state = add_collectible_func(state)
    return state
