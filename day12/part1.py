from pathlib import Path
from operator import attrgetter


class Node:
    def __init__(self, height_char):
        height = ord(height_char) - ord("a")
        self.height = height
        self.tentative_distance = float("inf")
        self.connections = []

    def add_connection(self, node):
        if node.height <= self.height + 1:
            self.connections.append(node)


class Graph:
    def __init__(self, start_node, end_node, unvisited_set):
        self.start_node = start_node
        self.end_node = end_node
        self.unvisited_set = unvisited_set

    def get_closest_node(self):
        return min(self.unvisited_set, key=attrgetter("tentative_distance"))

    def find_shortest_path(self):
        self.start_node.tentative_distance = 0

        while self.unvisited_set:
            current_node = self.get_closest_node()
            self.unvisited_set.remove(current_node)

            for connection in current_node.connections:
                if connection in self.unvisited_set:
                    new_distance = current_node.tentative_distance + 1
                    if new_distance < connection.tentative_distance:
                        connection.tentative_distance = new_distance
            if current_node == self.end_node:
                break

        return self.end_node.tentative_distance


def parse_input(text):
    unvisited_set = set()
    node_grid = []
    for line in text.splitlines():
        row = []

        for char in line:
            if char == "S":
                start_node = Node("a")
                node = start_node
            elif char == "E":
                end_node = Node("z")
                node = end_node
            else:
                node = Node(char)
            row.append(node)
            unvisited_set.add(node)
        node_grid.append(row)

    for y, row in enumerate(node_grid):
        for x, node in enumerate(row):
            if x > 0:
                node.add_connection(row[x - 1])
            if x < len(row) - 1:
                node.add_connection(row[x + 1])
            if y > 0:
                node.add_connection(node_grid[y - 1][x])
            if y < len(node_grid) - 1:
                node.add_connection(node_grid[y + 1][x])

    return Graph(start_node, end_node, unvisited_set)


if __name__ == "__main__":
    text = Path("input.txt").read_text()

    graph = parse_input(text)

    print(graph.find_shortest_path())