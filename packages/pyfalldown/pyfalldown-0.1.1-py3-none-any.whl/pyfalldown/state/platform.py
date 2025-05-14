from dataclasses import dataclass

from .game_item import GameItem


@dataclass
class Platform(GameItem):
    half_width: int
    half_height: int
