import numpy as np
import constants as c

# The population is an array of <population_size> matrices, each of <grid_size> size
def generate_population(population_size, grid_size):
    return [np.random.randint(0, 256, (grid_size, grid_size, 3)) for _ in range(population_size)]

# The fitness is the similarity between the chromosome's
# pixels and the target color
def fitness(chromosome):
    diff = 0
    for pixel in chromosome:
        diff += np.sum(np.abs(pixel - c.TARGET_COLOR))
    
    # Return fitness, lower diff means higher fitness
    return 1 / (1 + diff)

# Roulette wheel selection
def select(population):
    # Compute fitness levels for each chromosome and total fitness
    fitness_levels = [fitness(chromosome) for chromosome in population]
    total_fitness = sum(fitness_levels)

    # Compute the fitness proportion from the total fitness for each chromosome
    # for usage in the roulette wheel selection such that a chromosome has a
    # greater chance of being chosen if it has a higher fitness
    fitness_proportions = [fitness_level / total_fitness for fitness_level in fitness_levels]

    # Generate random probability
    random_probability = np.random.random()

    # Start the roulette wheel process
    cumulative_probability = 0
    for i in range(len(fitness_proportions)):
        cumulative_probability += fitness_proportions[i]
        if random_probability < cumulative_probability:
            return population[i]
    return population[-1]

# Randomly choose each pixel either
# from parent1 or from parent2
def crossover(parent1, parent2):
    rows = len(parent1)
    cols = len(parent2)
    child = parent1.copy()
    for i in range(rows):
        for j in range(cols):
            if np.random.random() < 0.5:
                child[i][j] = parent2[i][j]
        
    return child

def mutate(chromosome, generation):
    # Get dimensions of chromosome
    rows = len(chromosome)
    cols = len(chromosome[0])

    # Increase mutation probability over time
    base_mutation_probability = 0.05
    max_mutation_probability = 0.2
    mutation_probability = base_mutation_probability + (max_mutation_probability - base_mutation_probability) * (generation / c.MAX_GENERATIONS)

    mutated_chromosome = chromosome.copy()
    for i in range(rows):
        for j in range(cols):
            if np.random.random() <= mutation_probability:
                # Generate pixel offset
                mutation = np.random.randint(-50, 51, 3)

                # Mutate chromosome
                mutated_chromosome[i][j] = np.clip(chromosome[i][j] + mutation, 0, 255)

    return mutated_chromosome

def get_fittest_chromosome(population):
    return max(list(population), key=fitness)