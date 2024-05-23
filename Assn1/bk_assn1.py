import sys
import csv
import time
import random

from itertools import combinations
from itertools import combinations as comb
from deap import base, creator, tools, algorithms


# Check for command-line argument
if len(sys.argv) < 3:
    print("Usage: python script.py <filename.csv> <coverage level T>")
    sys.exit(1)

filename = sys.argv[1]
T = int(sys.argv[2])  # Dynamically set the coverage level from command line

# Load configuration from a CSV file
def load_configuration(filename):
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            configuration = [list(map(int, row)) for row in reader]
        return configuration
    except Exception as e:
        print(f"Error reading the configuration file: {e}")
        sys.exit(1)

configuration = load_configuration(filename)
N = len(configuration)  # Number of rows in the configuration array
K = len(configuration[0])  # Number of variables (columns)
V = max(max(row) for row in configuration) + 1  # Assuming values are 0-indexed

# Fitness function to minimize the number of rows while maximizing coverage
def evaluate(individual):
    included_rows = [i for i in range(len(individual)) if individual[i] == 1]
    combinations = list(comb(range(K), T))
    all_combinations = {combination: set() for combination in combinations}

    for row in included_rows:
        for combination in combinations:
            values = tuple(configuration[row][i] for i in combination)
            all_combinations[combination].add(values)

    covered = sum(len(all_combinations[combination]) == V**T for combination in combinations)
    uncovered_combinations = len(combinations) * V**T - covered
    # Increase penalty for each uncovered combination
    return len(included_rows) + uncovered_combinations * 10,  # Increased penalty factor

# Set up DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=N)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxUniform, indpb=0.1)  # Uniform crossover
toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)  # Increased mutation rate
toolbox.register("select", tools.selTournament, tournsize=5)

# Algorithm parameters
population = toolbox.population(n=100)  # Increased population size
NGEN = 200  # Increased number of generations
CXPB, MUTPB = 0.7, 0.3  # Adjusted probabilities for crossover and mutation

# Running the algorithm with timing
start_time = time.time()
for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=CXPB, mutpb=MUTPB)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, len(population))
    if gen % 10 == 0:  # Logging every 10 generations
        best_fitness = tools.selBest(population, 1)[0].fitness.values
        print(f"Generation {gen}: Best Fitness = {best_fitness}")

elapsed_time = time.time() - start_time
best_ind = tools.selBest(population, 1)[0]
print('Best Individual:', best_ind)
print('Fitness:', best_ind.fitness.values)
print('Rows selected:', [i for i, bit in enumerate(best_ind) if bit == 1])
print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Coverage check
def check_coverage(selected_rows, configuration, t):
    column_combinations = combinations(range(len(configuration[0])), t)
    coverage = {comb: set() for comb in column_combinations}
    
    for comb in coverage:
        for row in selected_rows:
            value_tuple = tuple(configuration[row][i] for i in comb)
            coverage[comb].add(value_tuple)
    
    for comb, values in coverage.items():
        if len(values) < V**t:
            return False, coverage
    return True, coverage

selected_rows = [i for i, bit in enumerate(best_ind) if bit == 1]
is_covered, detailed_coverage = check_coverage(selected_rows, configuration, T)
print("Is fully covered:", is_covered)
if not is_covered:
    print("Coverage details for debugging:", detailed_coverage)
