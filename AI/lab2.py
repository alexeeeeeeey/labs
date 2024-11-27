import pygad
import random


CITY_NAMES = ["A", "B", "C", "D", "E", "F"]
DISTANCE_MATRIX = [
    [0.0, 1.0, 1.41421356, 2.23606798, 3.60555128, 3.0],
    [1.0, 0.0, 1.0, 1.41421356, 3.16227766, 3.16227766],
    [1.41421356, 1.0, 0.0, 1.0, 2.23606798, 2.23606798],
    [2.23606798, 1.41421356, 1.0, 0.0, 2.0, 2.82842712],
    [3.60555128, 3.16227766, 2.23606798, 2.0, 0.0, 2.0],
    [3.0, 3.16227766, 2.23606798, 2.82842712, 2.0, 0.0],
]
SOL_PER_POP = 100


def get_distance(city1: list, city2: list):
    return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5


def fitness_function(ga_instance, solution, solution_idx):
    total_distance = 0

    if len(solution) != len(set(solution)):
        return -1e15

    for i in range(len(solution) - 1):
        city1 = int(solution[i])
        city2 = int(solution[i + 1])
        total_distance += DISTANCE_MATRIX[city1][city2]
    total_distance += DISTANCE_MATRIX[int(solution[-1])][int(solution[0])]

    return -total_distance


def create_initial_population(num_cities, sol_per_pop):
    population = []
    for _ in range(sol_per_pop):
        individual = random.sample(range(num_cities), num_cities)
        population.append(individual)
    return population


def main():
    initial_population = create_initial_population(
        len(CITY_NAMES), SOL_PER_POP
    )

    ga_instance = pygad.GA(
        num_generations=100,
        num_parents_mating=70,
        fitness_func=fitness_function,
        sol_per_pop=SOL_PER_POP,
        num_genes=len(CITY_NAMES),
        parent_selection_type="rws",
        keep_parents=70,
        initial_population=initial_population,
        mutation_type="swap",
        suppress_warnings=True,
        mutation_percent_genes=30,
    )

    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    optimal_route = [CITY_NAMES[int(gen)] for gen in solution]

    print("Оптимальный маршрут:", optimal_route)
    print("Длина оптимального маршрута:", -solution_fitness)


if __name__ == "__main__":
    main()
