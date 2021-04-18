import numpy as np
import itertools


def generate_outside_swap_combinations(path, out):
    return [[i, j] for i in range(len(path)) for j in range(len(out))]


def generate_inside_swap_edge_combinations(path):
    combinations = itertools.combinations(np.arange(len(path)), 2)
    return np.array([[v1, v2] for v1, v2 in combinations if 1 < v2 - v1 < len(path) - 1], 'int')