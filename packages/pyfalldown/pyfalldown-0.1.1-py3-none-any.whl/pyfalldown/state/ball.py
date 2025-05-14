from dataclasses import dataclass

from .game_item import GameItem


@dataclass
class Ball(GameItem):
    radius: int
