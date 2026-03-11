import random
import numpy as np
import time
from utils import load_distance_matrix

# Parameters
SN = 20
limit = 5
iterations = 1000
p = 100

# Fix random seed
random.seed(42)
np.random.seed(42)

distance_matrix = load_distance_matrix("matrix_3000.txt")
n = len(distance_matrix)

def fitness(centers):
    return max(min(distance_matrix[i][c] for c in centers) for i in range(n))

def random_solution():
    return sorted(random.sample(range(n), p))

def method2_neighbor(solution):
    new_sol = solution[:]
    to_remove = random.choice(new_sol)
    candidates = [i for i in range(n) if i not in new_sol]
    if not candidates:
        return new_sol
    to_add = random.choice(candidates)
    new_sol.remove(to_remove)
    new_sol.append(to_add)
    return sorted(new_sol)

def hybrid_abc():
    population = [random_solution() for _ in range(SN)]
    fitnesses = [fitness(sol) for sol in population]
    trials = [0] * SN

    best_fit = min(fitnesses)
    best_sol = population[fitnesses.index(best_fit)]

    start_time = time.time()

    for _ in range(iterations):
        # Employed bees
        for i in range(SN):
            neighbor = method2_neighbor(population[i])
            neighbor_fit = fitness(neighbor)
            if neighbor_fit < fitnesses[i]:
                population[i] = neighbor
                fitnesses[i] = neighbor_fit
                trials[i] = 0
            else:
                trials[i] += 1

        # Onlookers
        fitness_sum = sum(1 / (1 + f) for f in fitnesses)
        probs = [(1 / (1 + f)) / fitness_sum for f in fitnesses]
        for _ in range(SN):
            i = random.choices(range(SN), weights=probs, k=1)[0]
            neighbor = method2_neighbor(population[i])
            neighbor_fit = fitness(neighbor)
            if neighbor_fit < fitnesses[i]:
                population[i] = neighbor
                fitnesses[i] = neighbor_fit
                trials[i] = 0
            else:
                trials[i] += 1

        # Scout
        for i in range(SN):
            if trials[i] >= limit:
                population[i] = random_solution()
                fitnesses[i] = fitness(population[i])
                trials[i] = 0

        current_best = min(fitnesses)
        if current_best < best_fit:
            best_fit = current_best
            best_sol = population[fitnesses.index(current_best)]

    end_time = time.time()
    print("\nABC Final Best Solution:", best_sol)
    print("ABC Final Fitness:", best_fit)
    print(f"ABC Time Taken: {end_time - start_time:.4f} sec")

if __name__ == "__main__":
    hybrid_abc()
