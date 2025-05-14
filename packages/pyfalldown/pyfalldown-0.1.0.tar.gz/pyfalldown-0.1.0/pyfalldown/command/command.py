from collections.abc import Callable
from typing import Concatenate, ParamSpec

from pyfalldown.state import State

P = ParamSpec("P")

StateFunc = Callable[Concatenate[State, P], State]

Command = Callable[[State], State]


def wrap(f: StateFunc[P], *args: P.args, **kwargs: P.kwargs) -> Command:
    def wrapper(state: State) -> State:
        return f(state, *args, **kwargs)

    return wrapper
