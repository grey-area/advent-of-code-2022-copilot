from pathlib import Path


# class for range object
class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    # method for determining if the ranges share any numbers
    def overlaps(self, other):
        return self.start <= other.end and self.end >= other.start


if __name__ == "__main__":
    # Loop over lines in input.txt, counting up ranges that overlap
    count = 0
    for line in Path("input.txt").read_text().splitlines():
        # Line is like "2-4,6-8", giving two ranges
        range1, range2 = line.split(",")

        # Parse ranges
        range1 = Range(*map(int, range1.split("-")))
        range2 = Range(*map(int, range2.split("-")))

        # Check for overlap
        if range1.overlaps(range2):
            count += 1

    print(count)