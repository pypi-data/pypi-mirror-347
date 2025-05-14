from pyfalldown.state import Collectible, Platform, State


def scroll(state: State, step: int) -> State:
    state.platforms[:] = [
        Platform(p.x, p.y - step, p.half_width, p.half_height) for p in state.platforms if p.y + p.half_height > 0
    ]
    state.collectibles[:] = [Collectible([(x, y - step) for x, y in c.points], c.value) for c in state.collectibles]
    state.collectibles[:] = [c for c in state.collectibles if max(y for x, y in c.points) > 0]

    return state
