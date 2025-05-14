from dataclasses import dataclass, field

from .theme import Theme


@dataclass
class Config:
    theme: Theme = field(default_factory=Theme)
    gravity: int = 4
    ball_speed_x: int = 5
    scroll_speed: int = 2
    max_collectible_value: int = 5
