from pathlib import Path


class CPU:
    def __init__(self, inspect_cycles):
        self.x = 1
        self.clock = 0
        self.inspect_cycles = inspect_cycles
        self.recorded_signals = []

    def compute_signal(self):
        return self.clock * self.x

    def tick(self):
        self.clock += 1
        if self.clock in self.inspect_cycles:
            self.recorded_signals.append(self.compute_signal())

    def addx(self, v):
        self.tick()
        self.tick()
        self.x += v

    def noop(self):
        self.tick()

    def execute_instruction(self, instruction):
        if instruction.startswith('addx'):
            _, v = instruction.split(' ')
            self.addx(int(v))
        else:
            self.noop()


if __name__ == '__main__':
    inspect_cycles = [20, 60, 100, 140, 180, 220]
    cpu = CPU(inspect_cycles)

    for instruction in Path('input.txt').read_text().splitlines():
        cpu.execute_instruction(instruction)

    print(sum(cpu.recorded_signals))