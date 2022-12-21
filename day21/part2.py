from pathlib import Path
from operator import add, sub, mul, truediv
from dataclasses import dataclass
from typing import Callable
from fractions import Fraction


class Value:
    def __init__(self, m, c):
        self.m = Fraction(m)
        self.c = Fraction(c)

    def __add__(self, other):
        return Value(self.m + other.m, self.c + other.c)

    def __sub__(self, other):
        return Value(self.m - other.m, self.c - other.c)

    def __mul__(self, other):
        if self.m > 0 and other.m > 0:
            raise ValueError("Both sides in multiplication depend on humn")
        return Value(
            self.m * other.c + other.m * self.c,
            self.c * other.c
        )

    def __truediv__(self, other):
        if other.m > 0:
            raise ValueError("Right side in division depends on humn")
        return Value(self.m / other.c, self.c / other.c)

    def make_equal(self, other):
        result = (self.c - other.c) / (other.m - self.m)
        if result.denominator != 1:
            raise ValueError("Value is not an integer")
        return Value(m=0, c=result)


@dataclass(frozen=True)
class Operation:
    op: Callable[[Value, Value], Value]
    lhs: str
    rhs: str
    op_dict = {'+': add, '-': sub, '*': mul, '/': truediv, '=': Value.make_equal}


def solve(monkeys, name):
    job = monkeys[name]

    if name == "humn":
        ans = Value(m=1, c=0)
    elif isinstance(job, int):
        ans = Value(m=0, c=job)
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
        lhs, op_str, rhs = job.split()
        if name == "root":
            op_str = "="
        op = Operation.op_dict[op_str]
        job = Operation(op, lhs, rhs)

    return name, job


def parse_lines(filename):
    lines = Path(filename).read_text().splitlines()
    monkeys = {name: job for name, job in map(parse_line, lines)}
    return monkeys


if __name__ == "__main__":
    monkeys = parse_lines("input.txt")
    answer = solve(monkeys, "root").c.numerator
    print(answer)