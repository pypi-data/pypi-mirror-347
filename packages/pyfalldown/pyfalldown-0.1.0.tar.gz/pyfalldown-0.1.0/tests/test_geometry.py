from pyfalldown.geometry import polygon_circle_collision


def test_polygon_circle_collision() -> None:
    assert polygon_circle_collision((50, 50), 10, [(0, 0), (100, 0), (100, 100), (0, 100)])
    assert polygon_circle_collision((0, 0), 1, [(0, 0), (100, 0), (100, 100), (0, 100)])
    assert polygon_circle_collision((-10, -10), 10, [(0, 0), (100, 0), (100, 100), (0, 100)])
    assert not polygon_circle_collision((100, 50), 5, [(0, 0), (100, 0), (100, 100), (0, 100)])
    assert not polygon_circle_collision((150, 150), 20, [(0, 0), (100, 0), (100, 100), (0, 100)])
