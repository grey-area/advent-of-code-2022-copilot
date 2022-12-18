from dataclasses import dataclass
from pathlib import Path
import re
from itertools import combinations


@dataclass(frozen=True)
class ValveNode:
    name: str
    flow: int
    connects_to: set

    def __str__(self):
        return f"ValveNode(name={self.name}, flow={self.flow})"


class Graph:
    def find_shortest_path(self, start_node, end_node):
        visited = set()
        shortest_paths = {start_node: (None, 0)}
        current_node = start_node
        while current_node != end_node:
            visited.add(current_node)
            destinations = self.nodes_dict[current_node].connects_to
            weight_to_current_node = shortest_paths[current_node][1]
            for next_node in destinations:
                weight = weight_to_current_node + 1
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return None
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        path = path[::-1]
        return path

    def find_shortest_paths(self, visit_nodes):
        shortest_paths = {}
        for a, b in combinations(visit_nodes, 2):
            path = self.find_shortest_path(a, b)
            shortest_paths[(a, b)] = path
            shortest_paths[(b, a)] = path
        return shortest_paths

    def __init__(self, nodes_dict):
        self.nodes_dict = nodes_dict
        self.start_node = 'AA'
        self.nonzero_nodes = {name for name, node in nodes_dict.items() if node.flow > 0}
        self.shortest_paths = self.find_shortest_paths(self.nonzero_nodes | {self.start_node})

    def path_generator_helper(self, path, unvisited_nodes, time=30, score=0):
        if not unvisited_nodes:
            yield score, path
        else:
            for node in unvisited_nodes:
                new_path = path + [node]
                new_unvisited_nodes = unvisited_nodes - {node}
                duration = len(self.shortest_paths[(path[-1], node)])
                new_time = time - duration
                if new_time >= 0:
                    step_score = self.nodes_dict[node].flow * new_time
                    new_score = score + step_score
                    yield from self.path_generator_helper(new_path, new_unvisited_nodes, new_time, new_score)
                else:
                    yield score, path

    # yield all permutations of nonzero nodes, starting with the start node
    # do this recursively
    def path_generator(self):
        yield from self.path_generator_helper([self.start_node], self.nonzero_nodes)


def parse_line(line):
    # pattern to match input like following line
    # Valve SY has flow rate=0; tunnels lead to valves OJ, RZ
    line_pattern = re.compile(r"Valve (?P<name>\w+) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<connects_to_str>\w+(?:, \w+)*)")
    # pattern to find all valve names in the connects_to_str
    valve_pattern = re.compile(r"\w+")

    match = line_pattern.match(line)
    if match:
        name = match.group("name")
        flow = int(match.group("flow"))
        connects_to_str = match.group("connects_to_str")
        connects_to = set(valve_pattern.findall(connects_to_str))
        valve = ValveNode(name, flow, connects_to)
    else:
        raise ValueError(f"Line '{line}' does not match the pattern")
    return name, valve


def parse_input(filename):
    text = Path(filename).read_text()
    lines = text.splitlines()

    nodes_dict = {name: valve for name, valve in map(parse_line, lines)}
    graph = Graph(nodes_dict)
    return graph


if __name__ == "__main__":
    graph = parse_input("input.txt")

    best_score = 0
    for score, path in graph.path_generator():
        best_score = max(best_score, score)

    print(best_score)
