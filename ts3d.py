"""ts3d.py

Use the simulated annealing algorithm to find an approximate
solution to the traveling salesman problem in 3D."""

import math
import random
from random import randrange
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

def make_random_points(n, width, height, depth):
    """Makes n random points in a given space size."""
    points = []
    for _ in range(n):
        points.append((randrange(width), randrange(height), randrange(depth)))

    return points

def make_point_clusters(positions, n, x, y, z):
    """Returns a list of random points generated x, y, and z about
    the cluster positions."""

    points = []

    # Iterate throught the clusters
    for pos in positions:
        cluster = make_random_points(n, x, y, z)
        # Apply offset
        cluster = [(pos[0]+i, pos[1]+j, pos[2]+k) for (i,j,k) in cluster]
        points.extend(cluster[:])

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
    zdiff = point1[2] - point2[2]

    return math.sqrt(xdiff**2 + ydiff**2 + zdiff**2)

if __name__ == '__main__':
    # Setup
    temp = 5000
    cooling_rate = 0.001
    clusters = [(20, 20, 20), (20, 80, 20), (80, 80, 80)]
    current_path = make_point_clusters(clusters, 10, 20, 20, 20)

    # Shuffle the list since it is already in a *decent order
    random.shuffle(current_path)

    # Keeps track of changes for file names
    iteration = 0
    last_temp = 5000 
    should_save = False

    cycles = 0

    while temp > 0.05:
        index1 = randrange(len(current_path))
        index2 = randrange(len(current_path))

        new_path = swap_elements(current_path, index1, index2)
        nd = score(new_path)
        d = score(current_path)
        delta_e = nd - d

        if delta_e < 0:
            current_path = new_path[:]
            iteration += 1
            should_save = True
        elif delta_e > 0:
            probability = math.exp(-1 * delta_e/temp)
            rand = randrange(1, 100)
            if rand < probability*100:
                current_path = new_path[:]
                iteration += 1
                should_save = True

        cycles += 1
        temp = 5000/(1+cycles)

        if temp < last_temp-0.1:
            last_temp = temp

   # Plot the final path
    x = [a for (a, b, c) in current_path]
    y = [b for (a, b, c) in current_path]
    z = [c for (a, b, c) in current_path]

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(x, y, z)
    ax.plot3D(x, y, z)
    plt.show()

if False:
    if should_save:
        x = [a for (a, b, c) in current_path]
        y = [b for (a, b, c) in current_path]
        z = [c for (a, b, c) in current_path]

        fig = plt.figure()
        ax = plt.axes(projection='3d')

        ax.scatter3D(x, y, z)
        ax.plot3D(x, y, z)
        plt.savefig(f"plots/path_{iteration}.png")
        plt.close()

