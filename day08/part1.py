import numpy as np
from pathlib import Path


# Positions that are greater than all values to their left
def compute_visible_from_left(grid):
    # Cumulative maximum from left to right, with a column of -1 on the left
    cumulative_max = np.maximum.accumulate(grid, axis=1)[:, :-1]
    cumulative_max = np.concatenate([-np.ones((grid.shape[0], 1)), cumulative_max], axis=1)
    return grid > cumulative_max


if __name__ == "__main__":
    # input.txt has a dense grid of digits, like:
    # 123
    # 456
    # 789
    # Load this into a 2D array
    with Path("input.txt").open() as f:
        grid = np.array([[int(c) for c in line.strip()] for line in f])

    visible = compute_visible_from_left(grid)
    visible |= compute_visible_from_left(grid[:, ::-1])[:, ::-1]
    visible |= compute_visible_from_left(grid.T).T
    visible |= compute_visible_from_left(grid.T[:, ::-1])[:, ::-1].T

    print(np.sum(visible))