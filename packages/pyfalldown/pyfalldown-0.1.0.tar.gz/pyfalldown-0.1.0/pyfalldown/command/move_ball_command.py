from pyfalldown.state import Ball, State, Velocity


def move_ball(state: State, velocity: Velocity, max_width: int) -> State:
    vx, vy = velocity.vx, velocity.vy
    x = max(state.ball.radius, min(max_width - state.ball.radius, state.ball.x + vx))
    next_bottom = state.ball.y + vy + state.ball.radius
    ball_left = state.ball.x - state.ball.radius
    ball_right = state.ball.x + state.ball.radius
    ball_width = state.ball.radius * 2
    landed = False
    y = state.ball.y
    for p in state.platforms:
        if p.y - p.half_height <= next_bottom <= p.y + p.half_height:
            overlap_left = max(ball_left, p.x - p.half_width)
            overlap_right = min(ball_right, p.x + p.half_width)
            overlap = max(0, overlap_right - overlap_left)

            if overlap >= 0.2 * ball_width:
                y = p.y - p.half_height - state.ball.radius
                vy = 0
                landed = True
                break

    if not landed:
        y += vy
    state.ball = Ball(x, y, state.ball.radius)
    return state
