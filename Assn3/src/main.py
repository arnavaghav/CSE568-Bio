import numpy as np
import random
import matplotlib.pyplot as plt

""" Parameters: 100 ants and run it with the following parameters: 
             αA = 0.75, αB = 0.75, 
             βA = 0.9, βB = 0.36, 
             λA = 0.009, λB = 0.038.
"""

# Constants
GRID_SIZE = 50
NUM_ANTS = 100
INITIAL_FOOD = 100

# Feeders and nest locations
NEST = (25, 5)
FEEDER_A = (10, 40)
FEEDER_B = (40, 40)

# Parameters
ALPHA_A = ALPHA_B = 0.75
BETA_A = 0.9
BETA_B = 0.36
LAMBDA_A = 0.009
LAMBDA_B = 0.038

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'uncommitted'

    def move(self):
        # Ant moves randomly to an adjacent grid square or stays in the same spot
        direction = random.choice([(0,0), (1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)])
        self.x = (self.x + direction[0]) % GRID_SIZE
        self.y = (self.y + direction[1]) % GRID_SIZE

    def update_state(self, feeders):
        for feeder in feeders:
            if (self.x, self.y) == (feeder.x, feeder.y):
                if feeder == feeders[0]:  # Feeder A
                    self.state = 'committed_A'
                else:  # Feeder B
                    self.state = 'committed_B'


class Feeder:
    def __init__(self, x, y, food):
        self.x = x
        self.y = y
        self.food = food

class Simulation:
    def __init__(self):
        self.ants = [Ant(NEST[0], NEST[1]) for _ in range(NUM_ANTS)]
        self.feeders = [Feeder(FEEDER_A[0], FEEDER_A[1], INITIAL_FOOD),
                        Feeder(FEEDER_B[0], FEEDER_B[1], INITIAL_FOOD)]
        self.ant_count_A = [0]
        self.ant_count_B = [0]
        self.food_A = [INITIAL_FOOD]
        self.food_B = [INITIAL_FOOD]

    def run_step(self):
        count_A = count_B = 0
        for ant in self.ants:
            ant.move()
            ant.update_state(self.feeders)
            if ant.state == 'committed_A':
                count_A += 1
            elif ant.state == 'committed_B':
                count_B += 1
        self.ant_count_A.append(count_A)
        self.ant_count_B.append(count_B)
        self.food_A.append(self.feeders[0].food)
        self.food_B.append(self.feeders[1].food)

    def plot_results(self):
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(self.ant_count_A, label='Feeder A')
        plt.plot(self.ant_count_B, label='Feeder B')
        plt.title('Number of Ants at Each Feeder')
        plt.xlabel('Time Steps')
        plt.ylabel('Number of Ants')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(self.food_A, label='Food at Feeder A')
        plt.plot(self.food_B, label='Food at Feeder B')
        plt.title('Food Remaining at Feeders')
        plt.xlabel('Time Steps')
        plt.ylabel('Food Units')
        plt.legend()

        plt.tight_layout()
        plt.show()

        # Save the figure to a file
        plt.savefig('ants_simulation_results.png')  # Specify your path and file name here
        
        plt.show()  # This will still display the plot



def main():
    sim = Simulation()
    for _ in range(1000):  # Simulate for 1000 time steps
        sim.run_step()
    
    # Plot the final state of the grid
    sim.plot_results()

if __name__ == "__main__":
    main()
