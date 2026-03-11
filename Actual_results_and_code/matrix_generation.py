import numpy as np

def generate_large_matrix(size=3000, filename="matrix_3000.txt"):
    np.random.seed(42)
    mat = np.random.randint(1, 300, size=(size, size))
    np.fill_diagonal(mat, 0)
    sym_mat = (mat + mat.T) // 2  

    with open(filename, "w") as f:
        for row in sym_mat:
            f.write(" ".join(map(str, row)) + "\n")
    import os
    print("Saving to:", os.getcwd())


generate_large_matrix()
