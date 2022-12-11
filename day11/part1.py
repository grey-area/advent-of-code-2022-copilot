import re
from pathlib import Path


class Monkey:
    def inspect(self, old):
        self.inspect_count += 1
        # perform the operation on the old value using eval
        new = eval(self.op_text)
        new = new // 3

        if new % self.divisor == 0:
            return new, self.true_monkey
        else:
            return new, self.false_monkey

    def turn(self):
        for old in self.items:
            yield self.inspect(old)
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __init__(self, text):
        # Pattern to match following sort of text (multiple lines):
        # Capture the items, operation, test, and receiving monkeys
        """
        Monkey 0:
          Starting items: 79, 98
          Operation: new = old * 19
          Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3
        """
        pattern = re.compile(
            r"Monkey\s\d+:\s+Starting\sitems:\s(?P<items>\d+(?:,\s\d+)*)\n"
            r"\s+Operation:\snew\s=\s(?P<operation>old\s(?:\*|\+)\s(?:\d+|old))"
            r"\s+Test:\sdivisible by (?P<divisor>\d+)"
            r"\s+If\strue:\sthrow\sto\smonkey\s(?P<true>\d+)"
            r"\s+If\sfalse:\sthrow\sto\smonkey\s(?P<false>\d+)"
        )

        match = pattern.match(text)
        if match is None:
            raise ValueError("Invalid monkey text")
        monkey_attr = match.groupdict()

        self.items = [int(item) for item in monkey_attr["items"].split(", ")]
        self.op_text = monkey_attr["operation"]
        self.divisor = int(monkey_attr["divisor"])
        self.true_monkey = int(monkey_attr["true"])
        self.false_monkey = int(monkey_attr["false"])
        self.inspect_count = 0


def do_round(monkeys):
    for i, monkey in enumerate(monkeys):
        for item, receiving_monkey in monkey.turn():
            monkeys[receiving_monkey].add(item)


if __name__ == "__main__":
    text = Path("input.txt").read_text()

    monkeys = []
    for monkey_text in text.split("\n\n"):
        monkeys.append(Monkey(monkey_text))

    for _ in range(20):
        do_round(monkeys)

    # Sort by inspect count
    monkeys.sort(key=lambda monkey: monkey.inspect_count, reverse=True)
    # Print the product of the first 2
    print(monkeys[0].inspect_count * monkeys[1].inspect_count)