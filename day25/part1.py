from pathlib import Path
from math import log, floor


def from_snafu_char(char):
    if char == "-":
        return -1
    elif char == "=":
        return -2
    return int(char)


def to_snafu_char(value):
    if value == -1:
        return "-"
    elif value == -2:
        return "="
    return str(value)


def make_snafu(value):
    highest_digit = floor(log(2 * value - 1) / log(5))

    snafu = []
    for n in range(highest_digit, -1, -1):
        num = (value + (5**n - 1) // 2) // 5**n
        value -= num * 5**n
        snafu.append(to_snafu_char(num))
    return "".join(snafu)


def parse_line(line):
    reversed_line = line[::-1]
    value = sum(from_snafu_char(char) * 5**n for n, char in enumerate(reversed_line))
    return value


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines()
    answer = sum(parse_line(line) for line in lines)
    answer_snafu = make_snafu(answer)
    print(answer_snafu)