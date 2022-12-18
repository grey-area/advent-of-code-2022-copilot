import numpy as np
from sklearn.neighbors import BallTree


if __name__ == "__main__":
    # Read comma separated data into a numpy array
    data = np.genfromtxt('input.txt', delimiter=',')

    # Create a BallTree
    tree = BallTree(data, metric='l1')

    # Count points within a radius of 1, subtract 1 to exclude the point itself
    covered_sides = tree.query_radius(data, r=1.5, count_only=True) - 1
    exposed_sides = 6 - covered_sides

    print(sum(exposed_sides))