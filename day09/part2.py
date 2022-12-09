from pathlib import Path


class Rope:
    def __init__(self, length, parent=None):
        self.pos = [0, 0]
        self.parent = parent

        if length==1:
            self.child = None
            self.tail_visited = {tuple(self.pos)}
        else:
            self.child = Rope(length - 1, parent=self)
            self.tail_visited = self.child.tail_visited

    def process_line(self, line):
        direction, distance = line.split(' ')
        distance = int(distance)

        sign = 1 if direction in ['R', 'D'] else -1
        dimension = 0 if direction in ['L', 'R'] else 1
        for _ in range(distance):
            self.pos[dimension] += sign
            self.child.update_tail()

    def update_tail(self):
        for dimension in [0, 1]:
            displacement = self.parent.pos[dimension] - self.pos[dimension]
            other_displacement = self.parent.pos[1 - dimension] - self.pos[1 - dimension]
            if abs(displacement) > 1:
                if other_displacement != 0:
                    self.pos[1 - dimension] += 1 if other_displacement > 0 else -1
                self.pos[dimension] += 1 if displacement > 0 else -1
        if self.child is not None:
            self.child.update_tail()
        else:
            self.tail_visited.add(tuple(self.pos))

if __name__ == "__main__":
    rope = Rope(length=10)

    for line in Path("input.txt").read_text().splitlines():
        rope.process_line(line)

    print(len(rope.tail_visited))