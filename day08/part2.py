import numpy as np
from pathlib import Path


def compute_num_visible_to_the_left(grid):
    result = np.zeros_like(grid, dtype=int)

    for i, column in enumerate(grid.T):
        if i == 0:
            continue
        column = column.reshape(-1, 1)
        grid_to_left = grid[:, :i][:, ::-1]
        cumulative_max = np.maximum.accumulate(grid_to_left, axis=1)
        blocking_tree = cumulative_max >= column
        blocking_tree[:, -1] = True
        visible_trees = np.argmax(blocking_tree, axis=1) + 1
        result[:, i] = visible_trees

    return result


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        grid = np.array([[int(c) for c in line.strip()] for line in f])

    left = compute_num_visible_to_the_left(grid)
    right = compute_num_visible_to_the_left(grid[:, ::-1])[:, ::-1]
    up = compute_num_visible_to_the_left(grid.T).T
    down = compute_num_visible_to_the_left(grid.T[:, ::-1])[:, ::-1].T

    scores = left * right * up * down
    print(np.max(scores))