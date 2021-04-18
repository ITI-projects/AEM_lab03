
def calculate_delta_distance(first_vert, second_vert):
    return first_vert + second_vert


def calculate_delta_outside(path, outside, index, distance_matrix):
    inside_index = index[0]
    outside_index = index[1]
    length = len(path)
    before = calculate_delta_distance(distance_matrix[path[(inside_index - 1) % length], path[inside_index]], distance_matrix[path[inside_index], path[(inside_index + 1) % length]])
    after = calculate_delta_distance(distance_matrix[path[(inside_index - 1) % length], outside[outside_index]], distance_matrix[outside[outside_index], path[(inside_index + 1) % length]])
    delta = before - after
    return delta


def calculate_delta_inside_edges(path, index, distance_matrix):
    inside_index = index[0]
    outside_index = index[1]
    length = len(path)
    before = calculate_delta_distance(distance_matrix[path[(inside_index - 1) % length], path[inside_index]], distance_matrix[path[outside_index], path[(outside_index + 1) % length]])
    after = calculate_delta_distance(distance_matrix[path[(inside_index - 1) % length], path[outside_index]], distance_matrix[path[inside_index], path[(outside_index + 1) % length]])
    delta = before - after
    return delta
