from pathlib import Path
import re
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


class RockCorner(Point):
    def __init__(self, x, y):
        super().__init__(x, y)

    # range from the min to the max + 1
    @staticmethod
    def get_range(start, end):
        if start < end:
            return range(start, end + 1)
        else:
            return range(end, start + 1)

    def find_intermediate_points(self, other):
        if self.x == other.x:
            return {(self.x, y) for y in self.get_range(self.y, other.y)}
        elif self.y == other.y:
            return {(x, self.y) for x in self.get_range(self.x, other.x)}
        else:
            raise ValueError("Points are not on the same line")


class Sand(Point):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.settled = False

    def update(self, occupied, floor):
        # Check if the floor is below us
        if self.y + 1 == floor:
            self.settled = True
        # First try to move down
        elif (self.x, self.y + 1) not in occupied:
            self.y += 1
        # Otherwise try to move left and down
        elif (self.x - 1, self.y + 1) not in occupied:
            self.x -= 1
            self.y += 1
        # Otherwise try to move right and down
        elif (self.x + 1, self.y + 1) not in occupied:
            self.x += 1
            self.y += 1
        # Otherwise we are settled
        else:
            self.settled = True


# Find all pairs of numbers on the line
def parse_line(line):
    rocks = set()
    prev_point = None
    pairs = re.findall(r"\d+,\d+", line)
    for pair in pairs:
        x, y = pair.split(",")
        point = RockCorner(int(x), int(y))
        if prev_point is not None:
            rocks |= prev_point.find_intermediate_points(point)
        prev_point = point
    return rocks


def parse_input(filename):
    rocks = set()
    lines = Path(filename).read_text().splitlines()
    for line in lines:
        rocks |= parse_line(line)
    floor = 2 + max(rocks, key=lambda p: p[1])[1]
    return rocks, floor


def print_cave(rocks, sand, floor):
    occupied = rocks | sand
    min_x = min(occupied, key=lambda p: p.x).x - 5
    max_x = max(occupied, key=lambda p: p.x).x + 5
    min_y = min(0, min(occupied, key=lambda p: p.y).y)
    max_y = floor
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Point(x, y) in rocks or y == floor:
                print("#", end="")
            elif Point(x, y) in sand:
                print("o", end="")
            else:
                print(".", end="")
        print()


def simulate_grain(occupied, floor):
    current_sand = Sand(500, 0)
    while not current_sand.settled:
        current_sand.update(occupied, floor)
    return current_sand


def simulate(rocks, floor):
    sand = set()

    while (500, 0) not in sand:
        grain = simulate_grain(rocks | sand, floor)
        sand.add((grain.x, grain.y))

    return sand


if __name__ == "__main__":
    rocks, floor = parse_input("input.txt")
    sand = simulate(rocks, floor)
    print(len(sand))