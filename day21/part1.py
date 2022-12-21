from pathlib import Path
from operator import add, sub, mul, floordiv
from dataclasses import dataclass
from typing import Callable


@dataclass
class Operation:
    lhs: str
    op: Callable[[int, int], int]
    rhs: str
    ops = {'+': add, '-': sub, '*': mul, '/': floordiv}

    def __post_init__(self):
        self.op = self.ops[self.op]


def solve(monkeys, name):
    job = monkeys[name]
    if isinstance(job, int):
        return job
    else:
        left_part = solve(monkeys, job.lhs)
        right_part = solve(monkeys, job.rhs)
        return job.op(left_part, right_part)


def parse_line(line):
    name, job = line.split(': ')

    if job.isnumeric():
        job = int(job)
    else:
        job = Operation(*job.split())

    return name, job


def parse_lines(filename):
    lines = Path(filename).read_text().splitlines()
    monkeys = {name: job for name, job in map(parse_line, lines)}
    return monkeys


if __name__ == "__main__":
    monkeys = parse_lines("input.txt")
    answer = solve(monkeys, "root")
    print(answer)