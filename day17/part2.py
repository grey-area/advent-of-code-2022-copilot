import numpy as np
from pathlib import Path
from itertools import cycle
from dataclasses import dataclass


# text is a grid of . and #. Turn into a numpy array of 0 and 1
def load_shape(text):
    return np.array([[1 if c == "#" else 0 for c in line] for line in text.split("\n")], dtype=np.bool)


def load_shapes():
    text = Path("shapes.txt").read_text()
    shapes_text = text.split("\n\n")
    return [load_shape(shape_text) for shape_text in shapes_text]



class Rock:
    def __init__(self, x, y, shape_array):
        self.x = x
        self.y = y
        self.shape_array = shape_array
        self.width = shape_array.shape[1]


@dataclass(frozen=True)
class StateKey:
    row: str
    jet_i: int
    shape_i: int

@dataclass(frozen=True)
class StateValue:
    settled_rocks: int
    answer: int

@dataclass(frozen=True)
class Cycle:
    length: int
    answer_change: int


class Tunnel:
    shapes = load_shapes()

    def extend_height(self):
        # stack zeros on top
        extend_height = self.positions.shape[0]
        self.positions = np.vstack((np.zeros_like(self.positions), self.positions))
        return extend_height

    def test_collision(self, x, y):
        if x < 0 or x + self.current_rock.width > self.width:
            return True

        rock_array = self.current_rock.shape_array
        height, width = rock_array.shape
        position_array = self.positions[y : y + height, x : x + width]
        return np.any(rock_array & position_array)

    def remove_rows(self):
        # Find first full row
        full_rows = np.all(self.positions, axis=1)
        first_full_row = np.argmax(full_rows)
        remove_index = first_full_row + 1
        num_rows_to_remove = self.positions.shape[0] - remove_index
        self.positions = self.positions[:remove_index]
        self.removed_rows += num_rows_to_remove

    def get_grid_state(self):
        relevant_part = self.positions[self.compute_highest_y():, :]
        return self.str_of_grid(relevant_part)

    def identify_loop(self):
        if self.cycle is None:
            grid_state = self.get_grid_state()
            state_key = StateKey(grid_state, self.jet_i, self.shape_i)
            state_value = StateValue(self.settled_rocks, self.current_answer)
            if state_key in self.state_history:
                old_state_value = self.state_history[state_key]
                cycle_length = self.settled_rocks - old_state_value.settled_rocks
                answer_change = self.current_answer - old_state_value.answer
                self.cycle = Cycle(cycle_length, answer_change)
            self.state_history[state_key] = state_value

    def settle_rock(self):
        height, width = self.current_rock.shape_array.shape
        x, y = self.current_rock.x, self.current_rock.y
        self.positions[
            y : y + height,
            x : x + width,
        ] |= self.current_rock.shape_array
        self.settled_rocks += 1
        self.remove_rows()
        self.answers.append(self.current_answer)
        self.identify_loop()

    def update(self):
        self.jet_i, jet = next(self.jet_iter)
        updated_x = self.current_rock.x + jet
        if not self.test_collision(updated_x, self.current_rock.y):
            self.current_rock.x = updated_x
        updated_y = self.current_rock.y + 1
        if not self.test_collision(self.current_rock.x, updated_y):
            self.current_rock.y = updated_y
        else:
            self.settle_rock()
            self.current_rock = self.spawn_rock()

    def compute_highest_y(self):
        return np.min(np.where(self.positions)[0])

    def spawn_rock(self):
        self.shape_i, shape = next(self.shapes_iter)
        highest_y = self.compute_highest_y()
        if highest_y < 10:
            highest_y += self.extend_height()
        return Rock(2, highest_y - 3 - shape.shape[0], shape)

    def init_positions(self, width):
        positions = np.zeros((10, width), dtype=np.bool)
        positions[-1, :] = True
        return positions

    def str_of_grid(self, positions):
        # print dense grid of # and .
        return "\n".join(
            "".join("#" if c else "." for c in line) for line in positions
        )

    def __str__(self):
        return self.str_of_grid(self.positions)

    @property
    def current_answer(self):
        return self.positions.shape[0] - self.compute_highest_y() - 1 + self.removed_rows

    def __init__(self, jets, width=7):
        self.width = width
        self.jet_iter = cycle(enumerate([1 if c == ">" else -1 for c in jets]))
        self.positions = self.init_positions(width)
        self.shapes_iter = cycle(enumerate(Tunnel.shapes))
        self.current_rock = self.spawn_rock()
        self.settled_rocks = 0
        self.removed_rows = 0
        self.jet_i = 0
        self.shape_i = 0
        self.state_history = {}
        self.answers = [self.current_answer]
        self.cycle = None


if __name__ == "__main__":
    jets = Path("input.txt").read_text()
    tunnel = Tunnel(jets)

    num_rocks = 1000000000000
    while tunnel.settled_rocks < num_rocks:
        tunnel.update()
        if tunnel.cycle is not None:
            break

    num_cycles = num_rocks // tunnel.cycle.length
    position_in_cycle = num_rocks % tunnel.cycle.length
    answer = num_cycles * tunnel.cycle.answer_change + \
        tunnel.answers[position_in_cycle]
    print(answer)