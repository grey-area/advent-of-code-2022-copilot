from pathlib import Path


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.buffer = [['.' for _ in range(width)] for _ in range(height)]

    def draw_pixel(self, sprite_x):
        if abs(sprite_x - self.x) < 2:
            self.buffer[self.y][self.x] = '#'

        self.x += 1
        if self.x == self.width:
            self.x = 0
            self.y = (self.y + 1) % self.height

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.buffer])


class CPU:
    def __init__(self):
        self.x = 1
        self.clock = 0
        self.display = Display(40, 6)

    def tick(self):
        self.clock += 1
        self.display.draw_pixel(self.x)

    def addx(self, V):
        self.tick()
        self.tick()
        self.x += int(V)

    def noop(self):
        self.tick()

    def execute_instruction(self, instruction):
        if instruction.startswith('addx'):
            _, v = instruction.split(' ')
            self.addx(int(v))
        else:
            self.noop()


if __name__ == '__main__':
    cpu = CPU()

    for instruction in Path('input.txt').read_text().splitlines():
        cpu.execute_instruction(instruction)

    print(cpu.display)