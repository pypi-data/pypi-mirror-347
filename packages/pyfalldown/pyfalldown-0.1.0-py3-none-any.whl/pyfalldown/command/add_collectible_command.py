import random

from pyfalldown.state import Collectible, State


def add_collectible(state: State, max_x: int, max_value: int, size: int = 10, triangle_prob: float = 0.5) -> State:
    if len(state.platforms) <= 4 or len(state.collectibles) >= 10:
        return state
    x = random.randint(size, max_x - size)
    y = state.platforms[-1].y + state.platforms[-2].y
    y //= 2
    value = random.randint(0, max_value)
    if random.random() < triangle_prob:
        points = [
            (x, y - size),
            (x - size, y + size),
            (x + size, y + size),
        ]
        state.collectibles[:] = [*state.collectibles, Collectible(points, value)]
    else:
        points = [
            (x - size, y - size),
            (x - size, y + size),
            (x + size, y + size),
            (x + size, y - size),
        ]
        state.collectibles[:] = [*state.collectibles, Collectible(points, -value)]
    return state
