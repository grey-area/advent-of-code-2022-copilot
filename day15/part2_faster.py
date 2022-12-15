import re
from dataclasses import dataclass
from pathlib import Path
from tqdm import tqdm


@dataclass
class Point:
    x: int
    y: int

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass
class Sensor(Point):
    x: int
    y: int
    closest_beacon: Point

    def __post_init__(self):
        self.distance_to_closest_beacon = self.distance(self.closest_beacon)


@dataclass
class Range:
    start: int
    end: int


def parse_line(line):
    # pattern to parse input like "Sensor at x=num, y=num: closest beacon is at x=num, y=num"
    pattern = re.compile(r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)")
    match = pattern.match(line)
    if match:
        return Sensor(
            int(match.group("sensor_x")),
            int(match.group("sensor_y")),
            Point(int(match.group("beacon_x")), int(match.group("beacon_y")))
        )
    else:
        raise ValueError(f"Could not parse line: {line}")


def parse_input(filename):
    lines = Path(filename).read_text().splitlines()
    return [parse_line(line) for line in lines]


def get_xranges(sensors, y):
    ranges = []
    for sensor in sensors:
        y_distance = abs(sensor.y - y)
        x_range = sensor.distance_to_closest_beacon - y_distance
        if x_range > 0:
            ranges.append(Range(sensor.x - x_range, sensor.x + x_range))
    return ranges


def find_missing_x(xranges, limit):
    missing_x = None

    xranges.sort(key=lambda x: x.start)
    start = xranges[0].start
    if start > 0:
        missing_x = 0
    end = xranges[0].end

    minimum_overlap = limit
    for xrange in xranges[1:]:
        if xrange.start <= end:
            overlap = end - xrange.start
            minimum_overlap = min(minimum_overlap, overlap)
            end = max(end, xrange.end)
        else:
            if missing_x is None:
                missing_x = end + 1

    if end < limit and missing_x is None:
        missing_x = limit

    return missing_x, minimum_overlap


def find_distress_beacon(sensors, limit):
    distress_beacon = None

    y = 0
    with tqdm(total=limit, miniters=1) as pbar:
        while y <= limit:
            xranges = get_xranges(sensors, y)
            missing_x, minimum_overlap = find_missing_x(xranges, limit)
            if missing_x is not None:
                distress_beacon = Point(missing_x, y)
                break
            delta_y = max(1, minimum_overlap // 2)
            y += delta_y
            pbar.update(delta_y)

    return distress_beacon


if __name__ == "__main__":
    sensors = parse_input("input.txt")
    distress_beacon = find_distress_beacon(sensors, limit=4000000)
    print(4000000 * distress_beacon.x + distress_beacon.y)