import matplotlib.pyplot as plt
import numpy as np
import genetic_algorithm as ga
import constants as c
import sys

# Create figure and axis
fig, ax = plt.subplots()

# Set figure title
fig.canvas.manager.window.wm_title("Canvas Evolution")

# Event handler to close the figure and stop the process
def on_close(event):
    sys.exit()
fig.canvas.mpl_connect('close_event', on_close)

def run_genetic_algorithm():
    # Generate initial random population
    current_population = ga.generate_population(c.POPULATION_SIZE, c.GRID_SIZE)
    im = ax.imshow(ga.get_fittest_chromosome(current_population))
    plt.pause(0.001)

    for generation in range(c.MAX_GENERATIONS):
        fittest_chromosome = ga.get_fittest_chromosome(current_population)

        if np.all(fittest_chromosome == c.TARGET_COLOR):
            plt.title(f'Target color reached!')
            break
        else:
            plt.title(f'Generation: {generation}')

        # Each iteration, a new population will be built
        new_population = []
        
        # Add elitism by keeping the fittest individual
        new_population.append(fittest_chromosome)

        # Create new population
        for _ in range(c.POPULATION_SIZE - 1):
            parent1 = ga.select(current_population)
            parent2 = ga.select(current_population)
            child = ga.crossover(parent1, parent2)
            mutated_child = ga.mutate(child, generation)
            new_population.append(mutated_child)
        
        current_population = new_population
        
        # Update image with the fittest chromosome of each generation
        im.set_data(ga.get_fittest_chromosome(current_population))

        # Run event loop to render the image
        plt.pause(0.001)

    # Keep the figure open
    plt.show()

run_genetic_algorithm()