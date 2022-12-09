from pathlib import Path


class Rope:
    def __init__(self):
        self.head = [0, 0]
        self.tail = [0, 0]
        self.tail_visited = set(tuple(self.tail))

    def process_line(self, line):
        direction, distance = line.split(' ')
        distance = int(distance)

        sign = 1 if direction in ['R', 'D'] else -1
        dimension = 0 if direction in ['L', 'R'] else 1
        for _ in range(distance):
            self.head[dimension] += sign
            self.update_tail()

    def update_tail(self):
        for dimension in [0, 1]:
            displacement = self.head[dimension] - self.tail[dimension]
            if abs(displacement) > 1:
                self.tail[1 - dimension] = self.head[1 - dimension]
                self.tail[dimension] += 1 if displacement > 0 else -1
                self.tail_visited.add(tuple(self.tail))

if __name__ == "__main__":
    rope = Rope()

    for line in Path("input.txt").read_text().splitlines():
        rope.process_line(line)

    print(len(rope.tail_visited))