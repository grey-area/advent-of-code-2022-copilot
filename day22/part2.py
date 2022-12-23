from pathlib import Path
import re
from dataclasses import dataclass
from itertools import cycle


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = [None, None, None, None]

    def __str__(self):
        return f"Node({self.x}, {self.y})"


@dataclass
class Edge:
    node: Node
    direction_change: int


class Journey:
    def join_faces(self, xs, ys, fxs, fys, dir1, dir2):
        if isinstance(xs, int):
            xs = cycle([xs])
        if isinstance(ys, int):
            ys = cycle([ys])

        dir2_after = (dir2 + 2) % 4
        direction_change = (dir2_after - dir1)

        for x, y in zip(xs, ys):
            other_x = fxs(x, y)
            other_y = fys(x, y)
            node = self.nodes.get((x, y))
            other_node = self.nodes.get((other_x, other_y))
            if node is not None and other_node is not None:
                node.neighbours[dir1] = Edge(other_node, direction_change)
                other_node.neighbours[dir2] = Edge(node, -direction_change)

    def parse_input(self, grid_text):
        lines = grid_text.splitlines()

        self.nodes = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == ".":
                    self.nodes[(x, y)] = Node(x, y)

        # for each node, find its neighbours
        for node in self.nodes.values():
            for i, (dx, dy) in enumerate([(1, 0), (0, 1), (-1, 0), (0, -1)]):
                x = node.x + dx
                y = node.y + dy
                neighbour = self.nodes.get((x, y))
                if neighbour is not None:
                    node.neighbours[i] = Edge(neighbour, 0)

        # Messy joining up of the edges
        # Top of B, bottom of F
        self.join_faces(
            xs=range(100, 150), ys=0,
            fxs=lambda x, y: x - 100, fys=lambda x, y: 199,
            dir1=3, dir2=1
        )
        # Top of A, left of F
        self.join_faces(
            xs=range(50, 100), ys=0,
            fxs=lambda x, y: 0, fys=lambda x, y: x + 100,
            dir1=3, dir2=2
        )
        # Right of B, right of E
        self.join_faces(
            xs=149, ys=range(0, 50),
            fxs=lambda x, y: 99, fys=lambda x, y: (49 - y) + 100,
            dir1=0, dir2=0
        )
        # Left of A, left of D
        self.join_faces(
            xs=50, ys=range(0, 50),
            fxs=lambda x, y: 0, fys=lambda x, y: (49 - y) + 100,
            dir1=2, dir2=2
        )
        # Left of C, top of D
        self.join_faces(
            xs=50, ys=range(50, 100),
            fxs=lambda x, y: y - 50, fys=lambda x, y: 100,
            dir1=2, dir2=3
        )
        # Bottom of B, right of C
        self.join_faces(
            xs=range(100, 150), ys=49,
            fxs=lambda x, y: 99, fys=lambda x, y: x - 50,
            dir1=1, dir2=0
        )
        # Bottom of E, right of F
        self.join_faces(
            xs=range(50, 100), ys=149,
            fxs=lambda x, y: 49, fys=lambda x, y: x + 100,
            dir1=1, dir2=0
        )

        self.node = self.nodes[(50, 0)]
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
            edge = self.node.neighbours[self.direction]
            self.node = edge.node
            self.direction = (self.direction + edge.direction_change) % 4
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