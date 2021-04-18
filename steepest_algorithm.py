from operator import itemgetter

from delta import *
from swap import *
import numpy as np


def SteepestEdgesAlgorithm(path, outside, matrix):
    combinations_to_swap_inside = generate_inside_swap_edge_combinations(path)
    combinations_to_swap_outside = generate_outside_swap_combinations(path, outside)
    best_delta_inside = 1
    best_delta_outside = 1
    while (best_delta_inside > 0) or (best_delta_outside > 0):

        all_deltas = []
        for index in range(len(combinations_to_swap_outside)):
            vertices_to_swap = combinations_to_swap_outside[index]
            delta = calculate_delta_outside(path, outside, vertices_to_swap, matrix)
            all_deltas.append(delta)
        best_delta_outside = np.max(all_deltas)
        best_index_outside = combinations_to_swap_outside[np.argmax(all_deltas)]

        all_deltas.clear()
        for index in range(len(combinations_to_swap_inside)):
            vertices_to_swap = combinations_to_swap_inside[index]
            delta = calculate_delta_inside_edges(path, vertices_to_swap, matrix)
            all_deltas.append(delta)
        best_delta_inside = np.max(all_deltas)
        best_index_inside = combinations_to_swap_inside[np.argmax(all_deltas)]

        if (best_delta_inside > 0) or (best_delta_outside > 0):
            if best_delta_outside > best_delta_inside:
                temp = path[best_index_outside[0]]
                path[best_index_outside[0]] = outside[best_index_outside[1]]
                outside[best_index_outside[1]] = temp
            else:
                a = path[best_index_inside[0]:best_index_inside[1] + 1]
                a = np.flip(a)
                path[best_index_inside[0]:best_index_inside[1] + 1] = a
        combinations_to_swap_inside = generate_inside_swap_edge_combinations(path)
        combinations_to_swap_outside = generate_outside_swap_combinations(path, outside)

    return path


def generate_candidates(path, outside, matrix):
    tab = []
    for i in range(len(path)):
        sorted_list = np.argsort(matrix[path[i]])[1:]
        five_closest = sorted_list[~np.in1d(sorted_list, outside)]
        for elem in five_closest[:5]:
            it = [i, path.tolist().index(elem)]
            it.sort()
            tab.append(it)
    tab = np.unique(np.array(tab), axis=0)
    return tab


def SteepestEdgesCanditatesAlgorithm(path, outside, matrix):

    combinations_to_swap_inside = generate_candidates(path, outside, matrix)
    combinations_to_swap_outside = generate_outside_swap_combinations(path, outside)
    best_delta_inside = 1
    best_delta_outside = 1
    while (best_delta_inside > 0) or (best_delta_outside > 0):

        all_deltas = []
        for index in range(len(combinations_to_swap_outside)):
            vertices_to_swap = combinations_to_swap_outside[index]
            delta = calculate_delta_outside(path, outside, vertices_to_swap, matrix)
            all_deltas.append(delta)
        best_delta_outside = np.max(all_deltas)
        best_index_outside = combinations_to_swap_outside[np.argmax(all_deltas)]

        all_deltas.clear()

        best_delta_inside = 0
        best_index_inside = 0
        for id in range(len(combinations_to_swap_inside)):
            vertices_to_swap = [combinations_to_swap_inside[id][0], (combinations_to_swap_inside[id][1] - 1) % 100]
            delta = calculate_delta_inside_edges(path, vertices_to_swap, matrix)
            if delta > best_delta_inside:
                best_delta_inside = delta
                best_index_inside = vertices_to_swap

            vertices_to_swap = [(combinations_to_swap_inside[id][0] + 1) % 100, combinations_to_swap_inside[id][1]]
            delta = calculate_delta_inside_edges(path, vertices_to_swap, matrix)
            if delta > best_delta_inside:
                best_delta_inside = delta
                best_index_inside = vertices_to_swap

        if (best_delta_inside > 0) or (best_delta_outside > 0):
            if best_delta_outside > best_delta_inside:
                temp = path[best_index_outside[0]]
                path[best_index_outside[0]] = outside[best_index_outside[1]]
                outside[best_index_outside[1]] = temp
            else:
                a = path[best_index_inside[0]:best_index_inside[1] + 1]
                a = np.flip(a)
                path[best_index_inside[0]:best_index_inside[1] + 1] = a
        combinations_to_swap_inside = generate_candidates(path, outside, matrix)
        combinations_to_swap_outside = generate_outside_swap_combinations(path, outside)

    return path


def generate_outside_swap_combinations2(path, out, matrix):
    return [[i, j, calculate_delta_outside(path,out,[i,j],matrix)] for i in range(len(path)) for j in range(len(out))
            if calculate_delta_outside(path,out,[i,j],matrix) >0 ]


def generate_outside_swap_combinations3(path, i,  out, matrix):
    return [[i[0], j, calculate_delta_outside(path,out,[i[0],j],matrix)] for j in range(len(out))
            if calculate_delta_outside(path,out,[i[0],j],matrix)]


def generate_inside_swap_edge_combinations2(path, matrix):
    combinations = itertools.combinations(np.arange(len(path)), 2)
    return np.array([[v1, v2, calculate_delta_inside_edges(path, [v1, v2], matrix)] for v1, v2 in combinations if 1 < v2 - v1 < len(path) - 1
                     and calculate_delta_inside_edges(path, [v1, v2], matrix) > 0], 'int')


def generate_inside_swap_edge_combinations3(path, v, matrix):
    combinations = itertools.combinations(np.arange(len(path)), 2)
    return np.array([[v1, v2, calculate_delta_inside_edges(path, [v1, v2], matrix)] for v1, v2 in combinations if 1 < v2 - v1 < len(path) - 1 and
                     v1 == v[0] and calculate_delta_inside_edges(path, [v1, v2], matrix) > 0], 'int')


def SteepestEdgesCacheAlgorithm(path, outside, matrix):
    combinations_to_swap_inside = generate_inside_swap_edge_combinations2(path, matrix)
    combinations_to_swap_outside = generate_outside_swap_combinations2(path, outside, matrix)

    best_delta_inside = 1
    best_delta_outside = 1
    while (best_delta_inside > 0) or (best_delta_outside > 0):
        combinations_to_swap_outside = sorted(combinations_to_swap_outside, key=itemgetter(2))

        best_delta_outside = combinations_to_swap_outside[-1][2]
        best_index_outside = combinations_to_swap_outside[-1]

        combinations_to_swap_inside = sorted(combinations_to_swap_inside.tolist(), key=itemgetter(2))
        try:
            best_delta_inside = combinations_to_swap_inside[-1][2]
            best_index_inside = combinations_to_swap_inside[-1]
        except Exception:
            best_delta_inside = -100

        if (best_delta_inside > 0) or (best_delta_outside > 0):
            if best_delta_outside > best_delta_inside:
                temp = path[best_index_outside[0]]
                combinations_to_swap_outside = [i for i in combinations_to_swap_outside if i[0] != best_index_outside[0] and
                                                i[0] != (best_index_outside[0]+1)%100 and i[0] != best_index_outside[0]-1]
                path[best_index_outside[0]] = outside[best_index_outside[1]]
                outside[best_index_outside[1]] = temp
                combinations_to_swap_outside += generate_outside_swap_combinations3(path, [best_index_outside[0]], outside, matrix)
                combinations_to_swap_outside += generate_outside_swap_combinations3(path, [best_index_outside[0]-1], outside, matrix)
                combinations_to_swap_outside += generate_outside_swap_combinations3(path, [(best_index_outside[0]+1)%100], outside, matrix)
                combinations_to_swap_inside = generate_inside_swap_edge_combinations2(path, matrix)
            else:
                a = path[best_index_inside[0]:best_index_inside[1] + 1]
                a = np.flip(a)
                path[best_index_inside[0]:best_index_inside[1] + 1] = a
                combinations_to_swap_outside = [i for i in combinations_to_swap_outside if
                                                i[0] != best_index_inside[0] and
                                                i[0] != (best_index_inside[0] + 1) % 100 and i[0] !=
                                                best_index_inside[0] - 1 and
                                                i[0] !=( best_index_inside[1]+1)%100 and
                                                i[0] != (best_index_inside[1] + 2) % 100 and i[0] !=
                                                best_index_inside[1]
                                                ]
                combinations_to_swap_outside += generate_outside_swap_combinations3(path, [best_index_inside[0]], outside, matrix)
                combinations_to_swap_outside += generate_outside_swap_combinations3(path, [best_index_inside[0]-1], outside, matrix)
                combinations_to_swap_outside += generate_outside_swap_combinations3(path, [(best_index_inside[0]+1)%100], outside, matrix)
                combinations_to_swap_outside += generate_outside_swap_combinations3(path, [(best_index_inside[1])%100], outside, matrix)
                combinations_to_swap_outside += generate_outside_swap_combinations3(path, [best_index_inside[1]-1], outside, matrix)
                combinations_to_swap_outside += generate_outside_swap_combinations3(path, [(best_index_inside[1]+1)%100], outside, matrix)

                combinations_to_swap_inside = [i for i in combinations_to_swap_inside if
                                                i[0] != best_index_inside[0] and
                                                i[0] != (best_index_inside[0] + 1) % 100 and
                                                i[0] != (best_index_inside[1] + 1) % 100 and i[0] !=
                                               (best_index_inside[1]+2)%100
                                                ]
                combinations_to_swap_inside = np.asarray(combinations_to_swap_inside)
                try:
                    combinations_to_swap_inside = np.concatenate((combinations_to_swap_inside, generate_inside_swap_edge_combinations3(path, [best_index_inside[0]], matrix)))
                    combinations_to_swap_inside = np.concatenate((combinations_to_swap_inside, generate_inside_swap_edge_combinations3(path, [(best_index_inside[0]+1)%100], matrix)))
                    combinations_to_swap_inside = np.concatenate((combinations_to_swap_inside, generate_inside_swap_edge_combinations3(path, [(best_index_inside[1]+2)%100], matrix)))
                    combinations_to_swap_inside = np.concatenate((combinations_to_swap_inside, generate_inside_swap_edge_combinations3(path, [(best_index_inside[1]+1)%100], matrix)))
                except ValueError:
                    pass
    return path
