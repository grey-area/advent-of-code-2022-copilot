from pathlib import Path


class Node:
    def __init__(self, value, prev, length):
        self.value = value
        self.prev = prev
        self.next = None
        self.length = length

    def lookahead(self, n):
        node = self
        for _ in range(n):
            node = node.next
        return node

    def mix(self):
        # Find the node to insert after
        lookahead_value = self.value % (self.length - 1)
        node_to_insert_after = self.lookahead(lookahead_value)
        node_to_insert_before = node_to_insert_after.next

        if self is not node_to_insert_after and self is not node_to_insert_before:
            # Remove self from the list
            self.prev.next = self.next
            self.next.prev = self.prev

            # Insert self into the list
            node_to_insert_after.next = self
            self.prev = node_to_insert_after
            node_to_insert_before.prev = self
            self.next = node_to_insert_before


class Message:
    def __init__(self, nodes, zero_node):
        self.nodes = nodes
        self.zero_node = zero_node

    def get_answer(self):
        indices = [1000, 2000, 3000]
        answer = sum(self.zero_node.lookahead(i).value for i in indices)
        return answer

    def mix(self):
        for node in self.nodes:
            node.mix()


def parse_input(filename, decryption_key):
    lines = Path(filename).read_text().splitlines()
    length = len(lines)
    zero_node = None

    nodes = []
    prev = None
    for line in lines:
        value = int(line) * decryption_key
        node = Node(value, prev, length)
        if prev is not None:
            prev.next = node
        prev = node
        nodes.append(node)
        if value == 0:
            zero_node = node
    nodes[0].prev = nodes[-1]
    nodes[-1].next = nodes[0]
    return Message(nodes, zero_node)


if __name__ == "__main__":
    decryption_key = 811589153
    message = parse_input("input.txt", decryption_key)

    for _ in range(10):
        message.mix()

    answer = message.get_answer()
    print(answer)