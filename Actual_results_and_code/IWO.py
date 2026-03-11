import random
import numpy as np
import time
from utils import load_distance_matrix

# Parameters
ni = 5
nmax = 10
Xmin = 1
Xmax = 3
p = 100
Dmax = 3.0
Dmin = 0.5
iterations = 2000

random.seed(42)
np.random.seed(42)

distance_matrix = load_distance_matrix("matrix_3000.txt")
n = len(distance_matrix)

def fitness(centers):
    return max(min(distance_matrix[i][c] for c in centers) for i in range(n))

def random_solution():
    return sorted(random.sample(range(n), p))

def determine_seeds(Xmin, Xmax, ni, rank):
    g = Xmax - Xmin + 1
    s = ni / g
    group = int(rank // s)
    return max(Xmax - group, Xmin)

def compute_dradius(iteration, max_iter):
    return Dmax - ((Dmax - Dmin) * iteration / max_iter)

def generate_seed_dradius(parent, dradius):
    new_solution = []
    used = set()
    for c in parent:
        while True:
            delta = random.uniform(-1, 1) * dradius
            new_c = int(round(c + delta))
            new_c = max(0, min(n - 1, new_c))
            if new_c not in used:
                used.add(new_c)
                new_solution.append(new_c)
                break
    return sorted(new_solution)

def iwo_with_dradius():
    population = [random_solution() for _ in range(ni)]
    fitnesses = [fitness(sol) for sol in population]

    best_fit = min(fitnesses)
    best_sol = population[fitnesses.index(best_fit)]

    start_time = time.time()

    for iteration in range(1, iterations + 1):
        dr = compute_dradius(iteration, iterations)
        new_population = []
        new_fitnesses = []

        sorted_indices = sorted(range(len(population)), key=lambda i: fitnesses[i])

        for rank, idx in enumerate(sorted_indices):
            parent = population[idx]
            parent_fit = fitnesses[idx]
            num_seeds = determine_seeds(Xmin, Xmax, len(population), rank)

            new_population.append(parent)
            new_fitnesses.append(parent_fit)

            for _ in range(num_seeds):
                seed = generate_seed_dradius(parent, dr)
                seed_fit = fitness(seed)
                new_population.append(seed)
                new_fitnesses.append(seed_fit)

                if seed_fit < best_fit:
                    best_fit = seed_fit
                    best_sol = seed

        combined = list(zip(new_population, new_fitnesses))
        combined.sort(key=lambda x: x[1])
        population = [sol for sol, _ in combined[:nmax]]
        fitnesses = [fit for _, fit in combined[:nmax]]

    end_time = time.time()
    print("\nIWO Final Best Solution:", best_sol)
    print("IWO Final Fitness:", best_fit)
    print(f"IWO Time Taken: {end_time - start_time:.4f} sec")

if __name__ == "__main__":
    iwo_with_dradius()
