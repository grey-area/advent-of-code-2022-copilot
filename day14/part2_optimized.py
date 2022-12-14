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


def simulate_grain(occupied, floor, start):
    current_sand = Sand(*start)
    history = []
    while not current_sand.settled:
        history.append((current_sand.x, current_sand.y))
        current_sand.update(occupied, floor)

    return current_sand, history[:-1]


def simulate(rocks, floor):
    occupied = rocks.copy()

    start_position = (500, 0)
    start_positions = [start_position]
    while start_position not in occupied:
        grain, history = simulate_grain(occupied, floor, start_positions[-1])
        if len(history) == 0:
            start_positions.pop()
        else:
            start_positions += history[1:]
        occupied.add((grain.x, grain.y))

    return occupied


if __name__ == "__main__":
    rocks, floor = parse_input("input.txt")
    occupied = simulate(rocks, floor)
    sand = occupied - rocks
    print(len(sand))