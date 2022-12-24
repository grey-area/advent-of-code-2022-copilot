from pathlib import Path
from dataclasses import dataclass
from collections import deque, defaultdict


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Direction:
    front: Point
    left: Point
    right: Point


class Elf:
    def __init__(self, position):
        self.position = position

    def move(self, directions, occupied):
        proposed_position = None
        free = True

        for direction in directions:
            front = self.position + direction.front
            if front not in occupied and \
                    self.position + direction.left not in occupied and \
                    self.position + direction.right not in occupied:
                if proposed_position is None:
                    proposed_position = front
            else:
                free = False

        if free:
            proposed_position = None

        return proposed_position


class Game:
    def parse_input(self, input_text):
        elves = []
        occupied = set()
        for y, line in enumerate(input_text.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    point = Point(x, y)
                    elves.append(Elf(point))
                    occupied.add(point)
        return elves, occupied

    def __init__(self, input_text):
        directions = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]
        self.directions = deque()
        for i in range(4):
            front = directions[i]
            i2 = 2 * (i // 2 + 1)
            left = front + directions[i2 % 4]
            right = front + directions[(i2 + 1) % 4]
            self.directions.append(Direction(front, left, right))

        self.elves, self.occupied = self.parse_input(input_text)

    def update(self):
        update_dict = defaultdict(list)

        for elf in self.elves:
            proposed_position = elf.move(self.directions, self.occupied)
            if proposed_position is not None:
                update_dict[proposed_position].append(elf)

        for new_position, elf_list in update_dict.items():
            if len(elf_list) > 1:
                continue
            elf = elf_list[0]
            self.occupied.remove(elf.position)
            self.occupied.add(new_position)
            elf.position = new_position

        self.directions.rotate(-1)

    def calculate_free_squares(self):
        min_x = min(elf.position.x for elf in self.elves)
        max_x = max(elf.position.x for elf in self.elves)
        min_y = min(elf.position.y for elf in self.elves)
        max_y = max(elf.position.y for elf in self.elves)
        area = (max_x - min_x + 1) * (max_y - min_y + 1)
        free_squares = area - len(self.occupied)
        return free_squares

    def run(self):
        for _ in range(10):
            self.update()
        return self.calculate_free_squares()

if __name__ == "__main__":
    input_text = Path("input.txt").read_text()
    game = Game(input_text)

    answer = game.run()
    print(answer)