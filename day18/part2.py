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

    def out_of_bounds(self):
        lower = -1
        upper = 21
        return (
            self.x < lower or self.x > upper or
            self.y < lower or self.y > upper or
            self.z < lower or self.z > upper
        )


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


class Steam:
    def __contains__(self, point):
        return point in self.finished_steam

    def __init__(self, lava, initial_point=Point(-1, -1, -1)):
        self.unfinished_steam = {initial_point}
        self.finished_steam = set()
        self.lava = lava
        self.occupied = self.unfinished_steam | self.lava
        self.directions = init_directions()

    def update_step(self):
        point = self.unfinished_steam.pop()
        self.finished_steam.add(point)
        for direction in self.directions:
            new_point = point + direction
            if new_point not in self.occupied and not new_point.out_of_bounds():
                self.unfinished_steam.add(new_point)
                self.occupied.add(new_point)

    def expand(self):
        while self.unfinished_steam:
            self.update_step()


if __name__ == "__main__":
    lava = parse_input("input.txt")
    directions = init_directions()

    steam = Steam(lava)
    steam.expand()

    exposed_sides = 0
    for point, direction in product(lava, directions):
        if point + direction in steam:
            exposed_sides += 1

    print(exposed_sides)