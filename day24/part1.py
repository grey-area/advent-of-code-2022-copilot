from pathlib import Path
from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mod__(self, other):
        return Point(self.x % other.x, self.y % other.y)


class Blizzard:
    dir_strs = {'>': Point(1, 0), '<': Point(-1, 0), '^': Point(0, -1), 'v': Point(0, 1)}

    def __init__(self, x, y, dir_str, width, height):
        self.position = Point(x, y)
        self.dir_str = dir_str
        self.direction = self.dir_strs[dir_str]
        self.dimensions = Point(width, height)

    def update(self):
        self.position = (self.position + self.direction) % self.dimensions


class Valley:
    def __init__(self, input_text):
        self.blizzards = []

        lines = input_text.splitlines()
        self.height = len(lines) - 2
        self.width = len(lines[0]) - 2

        self.allowed_points = set()
        occupied_points = set()
        for y, line in enumerate(input_text.splitlines()[1:-1]):
            for x, char in enumerate(line[1:-1]):
                if char in Blizzard.dir_strs:
                    blizzard = Blizzard(x, y, char, self.width, self.height)
                    self.blizzards.append(blizzard)
                    occupied_points.add(blizzard.position)
                self.allowed_points.add(Point(x, y))
        self.allowed_points.add(Point(0, -1))
        self.allowed_points.add(Point(self.width - 1, self.height))
        self.occupied_points = [occupied_points]

        self.initial_state = str(self)
        self.make_occupied_set_list()

    def update(self):
        occupied_points = set()
        for blizzard in self.blizzards:
            blizzard.update()
            occupied_points.add(blizzard.position)
        return occupied_points

    def make_occupied_set_list(self):
        while True:
            occupied_points = self.update()
            if str(self) == self.initial_state:
                break
            self.occupied_points.append(occupied_points)

    def __str__(self):
        grid_text = [[" "] * self.width for _ in range(self.height)]
        for blizzard in self.blizzards:
            grid_text[blizzard.position.y][blizzard.position.x] = blizzard.dir_str
        return "\n".join("".join(row) for row in grid_text)

    def find_paths(self):
        start = Point(0, -1)
        end = Point(self.width - 1, self.height)

        best_t = float("inf")
        queue = deque([(start, 0)])
        visited = set()
        while queue:
            position, t = queue.popleft()

            if t >= best_t:
                continue
            t_mod = t % len(self.occupied_points)
            if (position, t_mod) in visited:
                continue
            visited.add((position, t_mod))

            occupied_points = self.occupied_points[t_mod]
            if position in occupied_points:
                continue
            if position not in self.allowed_points:
                continue

            if position == end:
                best_t = min(best_t, t)
                yield t
            else:
                for dir in [Point(1, 0), Point(0, 1), Point(0, 0), Point(-1, 0), Point(0, -1)]:
                    queue.append((position + dir, t + 1))

    def compute_answer(self):
        return min(self.find_paths())


if __name__ == "__main__":
    input_text = Path("input.txt").read_text()
    valley = Valley(input_text)

    answer = valley.compute_answer()
    print(answer)