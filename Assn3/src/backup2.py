import os
import random
import numpy as np
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
        self.has_food = False

    def move(self):
        # Ant moves randomly to an adjacent grid square or stays in the same spot
        direction = random.choice([(0,0), (1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)])
        self.x = (self.x + direction[0]) % GRID_SIZE
        self.y = (self.y + direction[1]) % GRID_SIZE

    def update_state(self, feeders):
        for feeder in feeders:
            if (self.x, self.y) == (feeder.x, feeder.y):
                if feeder.food > 0 and not self.has_food:
                    # Take food from feeder
                    feeder.food -= 1
                    self.has_food = True
                elif self.has_food:
                    # Return food to feeder
                    feeder.food += 1
                    self.has_food = False
                self.state = 'committed_A' if feeder == feeders[0] else 'committed_B'

class Feeder:
    def __init__(self, x, y, food):
        self.x = x
        self.y = y
        self.food = food

class Simulation:
    def __init__(self, folder_name):
        self.ants = [Ant(NEST[0], NEST[1]) for _ in range(NUM_ANTS)]
        self.feeders = [Feeder(FEEDER_A[0], FEEDER_A[1], INITIAL_FOOD),
                        Feeder(FEEDER_B[0], FEEDER_B[1], INITIAL_FOOD)]
        self.ant_count_A = [0]
        self.ant_count_B = [0]
        self.uncommitted_ants = [NUM_ANTS]
        self.food_A = [INITIAL_FOOD]
        self.food_B = [INITIAL_FOOD]
        self.folder_name = folder_name

    def run_step(self):
        count_A = count_B = count_uncommitted = 0

        for ant in self.ants:
            ant.move()
            ant.update_state(self.feeders)
            if ant.state == 'committed_A':
                count_A += 1
            elif ant.state == 'committed_B':
                count_B += 1
            else:
                count_uncommitted += 1

        self.ant_count_A.append(count_A)
        self.ant_count_B.append(count_B)
        self.uncommitted_ants.append(count_uncommitted)
        self.food_A.append(self.feeders[0].food)
        self.food_B.append(self.feeders[1].food)

    def plot_grid(self, count):
        grid = np.zeros((GRID_SIZE, GRID_SIZE, 3), dtype=float)
        
        # Nest location
        grid[NEST[1], NEST[0], :] = [1, 0, 0]  # Red
        
        # Feeder locations
        grid[FEEDER_A[1], FEEDER_A[0], :] = [0, 1, 0]  # Green
        grid[FEEDER_B[1], FEEDER_B[0], :] = [0, 0, 1]  # Blue
        
        # Plot ants
        for ant in self.ants:
            if ant.state == 'committed_A':
                grid[ant.y, ant.x, :] = [0.5, 1, 0.5]  # Light green
            elif ant.state == 'committed_B':
                grid[ant.y, ant.x, :] = [0.5, 0.5, 1]  # Light blue
            elif ant.state == 'uncommitted':
                grid[ant.y, ant.x, :] = [1, 1, 1]  # White

        plt.imshow(grid, origin='lower')  # Set origin to 'lower' to flip the y-axis
        plt.title('Grid Visualization')
        plt.show()

        plt.savefig(os.path.join(self.folder_name, f'grid{count}.png'))


    def plot_results(self):

        plt.figure(figsize=(15, 5))

        # Plot 1: Number of ants by commitment
        plt.subplot(1, 3, 1)
        plt.plot(self.ant_count_A, color='green', label='Committed to Feeder A')
        plt.plot(self.ant_count_B, color='blue', label='Committed to Feeder B')
        plt.plot(self.uncommitted_ants, color='grey', label='Uncommitted')
        plt.title('Ant Commitment over Time')
        plt.xlabel('Time Steps')
        plt.ylabel('Number of Ants')
        plt.legend()

        # Plot 2: Food remaining at feeders
        plt.subplot(1, 3, 2)
        plt.plot(self.food_A, color='green', label='Food at Feeder A')
        plt.plot(self.food_B, color='blue', label='Food at Feeder B')
        plt.title('Food Remaining at Feeders')
        plt.xlabel('Time Steps')
        plt.ylabel('Food Units')
        plt.legend()

        # Plot 3: Ratio of committed to uncommitted ants
        plt.subplot(1, 3, 3)
        total_committed = np.array(self.ant_count_A) + np.array(self.ant_count_B)
        ratio_committed_uncommitted = np.zeros_like(total_committed, dtype=float)  # Ensure output is float
        np.divide(total_committed, self.uncommitted_ants, out=ratio_committed_uncommitted, where=self.uncommitted_ants!=0)
        plt.plot(ratio_committed_uncommitted, color='purple', label='Ratio of Committed to Uncommitted')
        plt.title('Commitment Ratio over Time')
        plt.xlabel('Time Steps')
        plt.ylabel('Ratio')
        plt.legend()

        plt.tight_layout()
        plt.savefig(os.path.join(self.folder_name, 'ants_simulation_results.png'))
        plt.show()


def find_available_folder(base_path='Experiment'):
    counter = 1
    while True:
        folder_name = f"{base_path}#{counter}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            return folder_name
        counter += 1

def main():
    sim = Simulation(find_available_folder())
    for step in range(1000):  # Simulate for 1000 time steps
        sim.run_step()
        if step % 50 == 0:  # Update grid plot every 100 steps
            sim.plot_grid(step)

    # Plot the final state of the grid
    sim.plot_results()

if __name__ == "__main__":
    main()
