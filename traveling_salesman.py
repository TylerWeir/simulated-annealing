"""traveling_salesman.py

Use the simulated annealing algorithm to optimize the traveling
salesman problem."""

import math
from random import randrange
import matplotlib.pyplot as plt

def make_random_points(n, width, height):
    """Makes n random points in a given space size."""
    points = []
    for _ in range(n):
        points.append((randrange(width), randrange(height)))

    return points

def score(points:[]):
    """Returns the distance of traveling to each subsequent point."""
    total_dist = 0

    # Traverse from element 1 to element -2
    for i in range(1, len(points)):
        total_dist += dist(points[i-1], points[i])

    return total_dist

def swap_elements(path, index1, index2):
    """Swaps two elements in a list and returns a new list."""
    new_path = path[:]

    tmp = new_path[index1]
    new_path[index1] = path[index2]
    new_path[index2] = tmp

    return new_path

def dist(point1, point2):
    """Returns the distance between two points."""
    xdiff = point1[0] - point2[0]
    ydiff = point1[1] - point2[1]

    return math.sqrt(xdiff**2 + ydiff**2)

if __name__ == '__main__':
    temp = 100
    cooling_rate = 0.001
    current_path = make_random_points(20, 100, 100)

    while temp > 0:
        index1 = randrange(len(current_path))
        index2 = randrange(len(current_path))

        new_path = swap_elements(current_path, index1, index2)
        delta_e = score(new_path) - score(current_path)

        if delta_e < 0:
            current_path = new_path[:]
        else:
            probability = math.exp(-1 * delta_e/temp)
            if randrange(100) < probability*100:
                current_path = new_path[:]

        temp -= cooling_rate

    x = [a for (a, b) in current_path]
    y = [b for (a, b) in current_path]

    plt.scatter(x, y)
    plt.plot(x, y)
    plt.show()
