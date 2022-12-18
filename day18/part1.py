from pathlib import Path
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


def parse_line(line):
    x, y, z = line.split(",")
    return Point(int(x), int(y), int(z))


def parse_input(filename):
    lines = Path(filename).read_text().splitlines()
    return {parse_line(line) for line in lines}


def init_directions():
    return [
        Point(1, 0, 0),
        Point(-1, 0, 0),
        Point(0, 1, 0),
        Point(0, -1, 0),
        Point(0, 0, 1),
        Point(0, 0, -1),
    ]


if __name__ == "__main__":
    points = parse_input("input.txt")
    directions = init_directions()

    exposed_sides = 0
    for point, direction in product(points, directions):
        if point + direction not in points:
            exposed_sides += 1

    print(exposed_sides)