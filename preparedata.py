import tsplib95 as tsp
import numpy as np
from scipy.spatial import distance_matrix

pathA = "kroA200.tsp"
pathB = "kroB200.tsp"


class PrepareData:

    def __init__(self, path):
        self.data = tsp.load_problem(path)
        self.coordinates = self.get_coords()
        self.distance_matrix = self.calculate_distance_matrix()

    def get_coords(self):
        cords_dict = self.data.node_coords
        coordinates = []
        for k in cords_dict.keys():
            coordinates.append(cords_dict.get(k))
        return np.array(coordinates)

    def calculate_distance_matrix(self):
        matrix_of_distances = distance_matrix(self.coordinates, self.coordinates)
        matrix_of_distances = np.rint(matrix_of_distances)
        matrix_of_distances = matrix_of_distances.astype(int)
        return matrix_of_distances
