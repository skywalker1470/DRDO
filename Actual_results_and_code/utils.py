# utils.py
import numpy as np

def load_distance_matrix(filename="matrix_3000.txt", size=2000):
    matrix = []
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            if size is not None and i >= size:
                break
            row = list(map(int, line.strip().split()))
            if size is not None:
                row = row[:size]
            matrix.append(row)
    return np.array(matrix)
