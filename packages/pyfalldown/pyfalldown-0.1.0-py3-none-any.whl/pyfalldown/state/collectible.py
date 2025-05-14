from dataclasses import dataclass


@dataclass
class Collectible:
    points: list[tuple[int, int]]
    value: int
