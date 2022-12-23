from pathlib import Path
import re


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = [None, None, None, None]

    def __str__(self):
        return f"Node({self.x}, {self.y})"


class Journey:
    def parse_input(self, grid_text):
        lines = grid_text.splitlines()
        height = len(lines)
        width = max(len(line) for line in lines)

        nodes = {}
        # for each y, get the min and max x
        # for each x, get the min and max y
        min_x = [width] * height
        max_x = [0] * height
        min_y = [height] * width
        max_y = [0] * width
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char in ".#":
                    min_x[y] = min(min_x[y], x)
                    max_x[y] = max(max_x[y], x)
                    min_y[x] = min(min_y[x], y)
                    max_y[x] = max(max_y[x], y)
                if char == ".":
                    nodes[(x, y)] = Node(x, y)

        # for each node, find its neighbours
        for node in nodes.values():
            for i, (dx, dy) in enumerate([(1, 0), (0, 1), (-1, 0), (0, -1)]):
                x = node.x + dx
                y = node.y + dy
                if dx != 0:
                    x = (x - min_x[y]) % (max_x[y] - min_x[y] + 1) + min_x[y]
                if dy != 0:
                    y = (y - min_y[x]) % (max_y[x] - min_y[x] + 1) + min_y[x]
                node.neighbours[i] = nodes.get((x, y))

        self.node = nodes[(min_x[0], 0)]
        self.grid_text = [list(line) for line in lines]

    def __init__(self, text):
        self.direction = 0
        self.directions = ['>', 'v', '<', '^']
        self.parse_input(text)

    def move(self, distance):
        self.grid_text[self.node.y][self.node.x] = self.directions[self.direction]

        if distance == 0 or self.node.neighbours[self.direction] is None:
            return
        else:
            self.node = self.node.neighbours[self.direction]
            return self.move(distance - 1)

    def update(self, instruction):
        if instruction == "R":
            self.direction = (self.direction + 1) % 4
        elif instruction == "L":
            self.direction = (self.direction - 1) % 4
        else:
            self.move(int(instruction))

    def compute_answer(self):
        answer = 1000 * (self.node.y + 1) + 4 * (self.node.x + 1) + self.direction
        return answer

    def __str__(self):
        return '\n'.join(''.join(line) for line in self.grid_text)


def parse_input(filename):
    text = Path(filename).read_text()
    grid_text, instructions = text.split("\n\n")
    journey = Journey(grid_text)
    return journey, instructions


def main(journey, instructions):
    pattern = re.compile(r"\d+|[RL]")
    for instruction in pattern.findall(instructions):
        journey.update(instruction)

    answer = journey.compute_answer()
    print(answer)


if __name__ == "__main__":
    journey, instructions = parse_input("input.txt")
    main(journey, instructions)