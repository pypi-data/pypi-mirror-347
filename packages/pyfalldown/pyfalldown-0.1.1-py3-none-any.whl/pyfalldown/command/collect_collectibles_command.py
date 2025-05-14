from pyfalldown.geometry import polygon_circle_collision
from pyfalldown.state import State


def collect_collectibles(state: State) -> State:
    center = (state.ball.x, state.ball.y)
    radius = state.ball.radius
    not_collected = [c for c in state.collectibles if not polygon_circle_collision(center, radius, c.points)]
    collected = [c for c in state.collectibles if polygon_circle_collision(center, radius, c.points)]
    state.collectibles[:] = not_collected
    for c in collected:
        state.score += c.value
    return state
