import pandas as pd
import numpy as np
from functools import partial
from deap import base, creator, tools, algorithms

# Load one of the input files as an example
file_path = './k=10-v=2.csv'  # Adjust the path according to your environment
df = pd.read_csv(file_path)
configurations = df.values.tolist()  # Convert DataFrame to list of lists

# Define the fitness function
def evaluate(individual, configurations, t=2, v=2):
    selected_configs = [configurations[i] for i, include in enumerate(individual) if include == 1]
    covered_combinations = set()
    for col1 in range(len(configurations[0])):
        for col2 in range(col1 + 1, len(configurations[0])):
            for config in selected_configs:
                combination = (config[col1], config[col2])
                covered_combinations.add(combination)
    total_combinations = v ** t
    uncovered_combinations = total_combinations * (len(configurations[0]) * (len(configurations[0]) - 1) / 2) - len(covered_combinations)
    return (uncovered_combinations,)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_bool", np.random.randint, 0, 2)
n_rows = df.shape[0]
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=n_rows)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", partial(evaluate, configurations=configurations, t=2, v=2))
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Adjusting mutation and crossover rates slightly
mutpb = 0.3  # Slight increase in mutation probability
cxpb = 0.6   # Slight increase in crossover probability

def main():
    pop = toolbox.population(n=300)  # Consider experimenting with population size
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=50, stats=stats, halloffame=hof, verbose=True)  # Adjust ngen as needed
    
    return pop, log, hof

if __name__ == "__main__":
    main()
