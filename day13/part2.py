from pathlib import Path
import json
from functools import cmp_to_key
from math import prod


def compare(a, b):
    if isinstance(a, int) and isinstance(b, list):
        a = [a]
    if isinstance(a, list) and isinstance(b, int):
        b = [b]

    if isinstance(a, int) and isinstance(b, int):
        if a > b:
            return 1
        elif a == b:
            return 0
        else:
            return -1
    elif isinstance(a, list) and isinstance(b, list):
        for a_item, b_item in zip(a, b):
            if result := compare(a_item, b_item):
                return result
        if result := compare(len(a), len(b)):
            return result
    else:
        raise TypeError(f"Cannot compare {a} and {b}")

    return 0


if __name__ == "__main__":
    lines = Path("input.txt").read_text().replace("\n\n", "\n").splitlines()
    packets = [json.loads(line) for line in lines]
    divider_packets = [[[2]], [[6]]]
    packets += divider_packets

    packets.sort(key=cmp_to_key(compare))

    divider_indices = [packets.index(p) + 1 for p in divider_packets]
    print(prod(divider_indices))