from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class ValveNode:
    name: str
    flow: int
    connects_to: set


class Graph:
    # Find shortest distance from start node to every other node
    def find_shortest_paths_from(self, start_node):
        tentative_distances = {node: float('inf') for node in self.nodes_dict}
        tentative_distances[start_node] = 0
        unvisited_nodes = set(self.nodes_dict)
        while unvisited_nodes:
            current_node = min(unvisited_nodes, key=lambda node: tentative_distances[node])
            unvisited_nodes.remove(current_node)
            for neighbor in self.nodes_dict[current_node].connects_to:
                if neighbor in unvisited_nodes:
                    new_distance = tentative_distances[current_node] + 1
                    if new_distance < tentative_distances[neighbor]:
                        tentative_distances[neighbor] = new_distance
        return {(start_node, node): distance for node, distance in tentative_distances.items()}

    def find_shortest_paths(self, visit_nodes):
        shortest_paths = {}
        for node in visit_nodes:
            shortest_paths.update(self.find_shortest_paths_from(node))
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
                duration = self.shortest_paths[(path[-1], node)] + 1
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

    def compute_answer(self):
        best_score = 0
        for score, _ in self.path_generator():
            best_score = max(best_score, score)
        return best_score


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

    answer = graph.compute_answer()
    print(answer)
