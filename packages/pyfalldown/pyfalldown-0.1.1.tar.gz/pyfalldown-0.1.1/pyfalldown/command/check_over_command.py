from pyfalldown.state import State


def check_over(state: State, max_height: int) -> State:
    ball_top = state.ball.y - state.ball.radius
    ball_bottom = state.ball.y + state.ball.radius
    if ball_top < 0 or ball_bottom > max_height:
        state.over = True
    return state
