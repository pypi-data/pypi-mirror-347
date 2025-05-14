from dataclasses import dataclass

from .ball import Ball
from .collectible import Collectible
from .platform import Platform


@dataclass
class State:
    ball: Ball
    platforms: list[Platform]
    collectibles: list[Collectible]
    score: int = 0
    over: bool = False
