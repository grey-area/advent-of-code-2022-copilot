from pathlib import Path
from operator import add, sub, mul, truediv
from dataclasses import dataclass
from typing import Callable
from fractions import Fraction


@dataclass
class Answer:
    m: Fraction
    c: Fraction

    def __post_init__(self):
        self.m = Fraction(self.m)
        self.c = Fraction(self.c)

    def __add__(self, other):
        return Answer(self.m + other.m, self.c + other.c)

    def __sub__(self, other):
        return Answer(self.m - other.m, self.c - other.c)

    def __mul__(self, other):
        if self.m > 0 and other.m > 0:
            raise ValueError("Both sides in multiplication depend on humn")
        return Answer(
            self.m * other.c + other.m * self.c,
            self.c * other.c
        )

    def __truediv__(self, other):
        if other.m > 0:
            raise ValueError("Right side in division depends on humn")
        return Answer(self.m / other.c, self.c / other.c)

    def make_equal(self, other):
        result = (self.c - other.c) / (other.m - self.m)
        if result.denominator != 1:
            raise ValueError("Answer is not an integer")
        return Answer(m=0, c=result)


@dataclass
class Operation:
    lhs: str
    op: Callable[[Answer, Answer], Answer]
    rhs: str
    ops = {'+': add, '-': sub, '*': mul, '/': truediv, '=': Answer.make_equal}

    def __post_init__(self):
        self.op = self.ops[self.op]


def solve(monkeys, name):
    job = monkeys[name]

    if name == "humn":
        ans = Answer(m=1, c=0)
    elif isinstance(job, int):
        ans = Answer(m=0, c=job)
    else:
        left_part = solve(monkeys, job.lhs)
        right_part = solve(monkeys, job.rhs)
        ans = job.op(left_part, right_part)
    return ans


def parse_line(line):
    name, job = line.split(': ')

    if job.isnumeric():
        job = int(job)
    else:
        lhs, op, rhs = job.split()
        if name == "root":
            op = "="
        job = Operation(lhs, op, rhs)

    return name, job


def parse_lines(filename):
    lines = Path(filename).read_text().splitlines()
    monkeys = {name: job for name, job in map(parse_line, lines)}
    return monkeys


if __name__ == "__main__":
    monkeys = parse_lines("input.txt")
    answer = solve(monkeys, "root")
    print(answer.c.numerator)