from pathlib import Path
import json


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
    text = Path("input.txt").read_text()
    pairs = text.split("\n\n")
    pairs = [[json.loads(packet) for packet in pair.splitlines()] for pair in pairs]

    comparisons = [compare(*pair) for pair in pairs]
    correct = [i + 1 for i, c in enumerate(comparisons) if c == -1]
    print(sum(correct))