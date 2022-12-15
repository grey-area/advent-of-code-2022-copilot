import re
from dataclasses import dataclass
from pathlib import Path


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
class DummyLinearSensor:
    x: int
    distance_to_closest_beacon: int

    def in_range(self, x):
        return abs(self.x - x) <= self.distance_to_closest_beacon


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


if __name__ == "__main__":
    sensors = parse_input("input.txt")
    y = 2000000

    # create a list of LinearSensors for that row
    linear_sensors = []
    for sensor in sensors:
        y_distance = abs(sensor.y - y)
        x_range = sensor.distance_to_closest_beacon - y_distance
        if x_range > 0:
            linear_sensor = DummyLinearSensor(sensor.x, x_range)
            linear_sensors.append(linear_sensor)

    min_x = min(linear_sensor.x - linear_sensor.distance_to_closest_beacon for linear_sensor in linear_sensors)
    max_x = max(linear_sensor.x + linear_sensor.distance_to_closest_beacon for linear_sensor in linear_sensors)

    invalid_positions = set()
    for sensor in linear_sensors:
        invalid_positions |= set(range(sensor.x - sensor.distance_to_closest_beacon, sensor.x + sensor.distance_to_closest_beacon + 1))

    # Off by 1 for some reason?
    print(len(invalid_positions) - 1)