import math
from collections.abc import Sequence

RealNumber = int | float
Point = tuple[RealNumber, RealNumber]
Segment = tuple[Point, Point]


def point_in_polygon(point: Point, polygon: Sequence[Point]) -> bool:
    x, y = point
    inside = False
    n = len(polygon)

    px1, py1 = polygon[0]
    for i in range(1, n + 1):
        px2, py2 = polygon[i % n]
        if ((py1 > y) != (py2 > y)) and (x < (px2 - px1) * (y - py1) / (py2 - py1) + px1):
            inside = not inside
        px1, py1 = px2, py2

    return inside


def distance_point_to_segment(point: Point, segment: Segment) -> RealNumber:
    px, py = point
    x1, y1 = segment[0]
    x2, y2 = segment[1]
    dx, dy = x1 - x2, y1 - y2
    if dx == dy == 0:
        return math.hypot(px - x1, px - x2)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    closest_x, closest_y = x1 + t * dx, y1 + t * dy
    return math.hypot(px - closest_x, py - closest_y)


def polygon_circle_collision(center: Point, radius: RealNumber, polygon: Sequence[Point]) -> bool:
    if point_in_polygon(center, polygon):
        return True
    for i in range(len(polygon)):
        p1, p2 = polygon[i], polygon[(i + 1) % len(polygon)]
        if distance_point_to_segment(center, (p1, p2)) <= radius:
            return True

    return False
