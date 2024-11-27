import numpy as np
import pygad

# Матрица расстояний между городами
distances = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

# Количество городов
num_cities = distances.shape[0]

# Пространство генов для каждого города
gene_space = [{'low': 0, 'high': num_cities - 1} for _ in range(num_cities)]

# Функция приспособленности (fitness function)
def fitness_func(ga_instance, solution, solution_idx):
    solution = np.round(solution).astype(int)  # Приводим решение к целым числам
    route_length = 0
    for i in range(num_cities - 1):
        route_length += distances[solution[i], solution[i + 1]]
    route_length += distances[solution[-1], solution[0]]  # Возвращаемся в начальный город

    if route_length == 0:
        return 0
    
    fitness = 1.0 / route_length
    return fitness

# Коллбэк для каждого поколения
def on_generation(ga_instance):
    print(f"Поколение: {ga_instance.generations_completed}")

# Генетический алгоритм
ga_instance = pygad.GA(
    num_generations=500,
    num_parents_mating=4,
    fitness_func=fitness_func,
    sol_per_pop=10,
    num_genes=num_cities,
    gene_space=gene_space,  # Пространство генов для каждого города
    mutation_percent_genes=10,
    mutation_num_genes=1,
    mutation_type="swap",
    crossover_type="scattered",  # Разрозненный кроссовер
    parent_selection_type="sss",
    keep_parents=2,
    on_generation=on_generation,
    allow_duplicate_genes=False  # Запрещаем дубликаты
)

# Запуск алгоритма
ga_instance.run()

# Получение лучшего решения
best_solution, best_solution_fitness, _ = ga_instance.best_solution()
best_route_length = 1.0 / best_solution_fitness

print("Лучший маршрут:", best_solution)
print("Длина лучшего маршрута:", best_route_length)
