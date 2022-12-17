import numpy as np
from pathlib import Path
from itertools import cycle
from tqdm import tqdm


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

    def settle_rock(self):
        height, width = self.current_rock.shape_array.shape
        x, y = self.current_rock.x, self.current_rock.y
        self.positions[
            y : y + height,
            x : x + width,
        ] |= self.current_rock.shape_array
        self.settled_rocks += 1

    def update(self):
        updated_x = self.current_rock.x + next(self.jet_iter)
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
        shape = next(self.shapes_iter)
        highest_y = self.compute_highest_y()
        if highest_y < 10:
            highest_y += self.extend_height()
        return Rock(2, highest_y - 3 - shape.shape[0], shape)

    def init_positions(self, width):
        positions = np.zeros((10, width), dtype=np.bool)
        positions[-1, :] = True
        return positions

    def __str__(self):
        # print dense grid of # and .
        return "\n".join(
            "".join("#" if c else "." for c in line) for line in self.positions
        )

    def __init__(self, jets, width=7):
        self.width = width
        self.jet_iter = cycle([1 if c == ">" else -1 for c in jets])
        self.positions = self.init_positions(width)
        self.shapes_iter = cycle(Tunnel.shapes)
        self.current_rock = self.spawn_rock()
        self.settled_rocks = 0


if __name__ == "__main__":
    jets = Path("input.txt").read_text()
    tunnel = Tunnel(jets)

    num_rocks = 2022
    with tqdm(total=num_rocks) as pbar:
        while tunnel.settled_rocks < num_rocks:
            tunnel.update()
            pbar.update(tunnel.settled_rocks - pbar.n)

    print(tunnel.positions.shape[0] - tunnel.compute_highest_y() - 1)