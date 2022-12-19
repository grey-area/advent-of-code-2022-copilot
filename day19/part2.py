from dataclasses import dataclass
from pathlib import Path
import re
from math import ceil, prod
from tqdm import tqdm


@dataclass(frozen=True)
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __add__(self, other):
        return Resources(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode,
        )

    def __sub__(self, other):
        return Resources(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode,
        )

    def __mul__(self, other):
        return Resources(
            self.ore * other,
            self.clay * other,
            self.obsidian * other,
            self.geode * other,
        )

    def steps_required(self, production):
        time_needed = 0
        for attr in self.__dataclass_fields__:
            numerator = getattr(self, attr)
            if numerator == 0:
                continue
            else:
                try:
                    attr_time_needed = ceil(numerator / getattr(production, attr))
                except ZeroDivisionError:
                    attr_time_needed = float("inf")
                time_needed = max(time_needed, attr_time_needed)
        return time_needed


@dataclass(frozen=True)
class RobotType:
    cost: Resources
    production: Resources


class Blueprint:
    def __init__(self, robot_types):
        self.robot_types = robot_types

    def produce(self, robot_counts):
        resources = Resources()
        for r, c in robot_counts.items():
            resources = resources + self.robot_types[r].production * c
        return resources

    def generate_strategies(self, robot_counts, resources_to_produce, remaining_time, resources=Resources()):
        if remaining_time == 0:
            yield resources.geode
        else:
            turn_production = self.produce(robot_counts)

            # remove robots that we don't need to build any more
            for resource_name in resources_to_produce:
                # maximum number of this resource required by any robot
                max_required_per_turn = max(getattr(robot_type.cost, resource_name) for robot_type in self.robot_types.values())
                current_production = robot_counts[resource_name]
                per_turn_production_shortfall = max_required_per_turn - current_production
                overall_production_shortfall = per_turn_production_shortfall * remaining_time
                current_resource = getattr(resources, resource_name)
                if overall_production_shortfall <= current_resource:
                    resources_to_produce = resources_to_produce - {resource_name}

            for robot_name in resources_to_produce | {'geode'}:
                robot = self.robot_types[robot_name]
                extra_resources_needed = robot.cost - resources
                time_needed = extra_resources_needed.steps_required(
                    turn_production
                ) + 1
                time_needed = min(time_needed, remaining_time)

                new_resources = resources + turn_production * time_needed - robot.cost
                new_robot_counts = robot_counts.copy()
                new_robot_counts[robot_name] += 1
                yield from self.generate_strategies(
                    new_robot_counts,
                    resources_to_produce,
                    remaining_time - time_needed,
                    new_resources
                )

    def generate_strategies_helper(self, time):
        robot_counts = {r: 0 for r in self.robot_types.keys()}
        robot_counts['ore'] = 1
        resources_to_produce = set(self.robot_types.keys())
        yield from self.generate_strategies(robot_counts, resources_to_produce, time)

    def get_score(self, time):
        return max(self.generate_strategies_helper(time))


def parse_cost_text(text):
    # pattern to find a number followed by a resource name, like "<num> <name>"
    matches = re.findall(r"(\d+) (\w+)", text)
    resource_dict = {m[1]: int(m[0]) for m in matches}
    return Resources(**resource_dict)


def parse_line(line):
    # Each <name> robot costs <text>.
    robot_types = {}

    matches = re.findall(r"Each (\w+) robot costs ([^\.]+)", line)
    for match in matches:
        robot_type_name = match[0]
        production = Resources(**{robot_type_name: 1})
        cost = parse_cost_text(match[1])
        robot_types[robot_type_name] = RobotType(cost, production)

    return Blueprint(robot_types)


def parse_input(filename):
    lines = Path(filename).read_text().splitlines()
    return [parse_line(line) for line in lines]


if __name__ == "__main__":
    blueprints = parse_input("input.txt")[:3]

    answer = prod(blueprint.get_score(32) for blueprint in tqdm(blueprints))
    print(answer)