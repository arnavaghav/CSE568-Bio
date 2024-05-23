import os
import random
import numpy as np
import matplotlib.pyplot as plt

# Constants
GRID_SIZE = 50
NUM_ANTS = 100
INITIAL_FOOD = 100
NEST = (25, 5)
FEEDER_A = (10, 40)
FEEDER_B = (35, 35)

ALPHA_A = ALPHA_B = 0.0225
BETA_A = 0.015   # Higher recruitment rate for the good feeder (Feeder A)
BETA_B = 0.006   # Lower recruitment rate for the poor feeder (Feeder B)
LAMBDA_A = 0.009  # Lower attrition rate for the good feeder (Feeder A)
LAMBDA_B = 0.038  # Higher attrition rate for the poor feeder (Feeder B)

global timesteps 
timesteps = 1000

# Parameters - Adjusted to favor Feeder A depletion
# ALPHA_A = 1.0  # Increased discovery rate for Feeder A
# ALPHA_B = 0.75  # Original rate for Feeder B
# BETA_A = 0.95   # Increased recruitment rate for Feeder A
# BETA_B = 0.36   # Original lower recruitment rate for Feeder B
# LAMBDA_A = 0.005  # Lower attrition rate for Feeder A, ants less likely to leave
# LAMBDA_B = 0.038  # Higher attrition rate for Feeder B, ants more likely to leave

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

    def update_state(self, feeders, ants):
        # Define nearby_ants at the start of the method
        nearby_ants = [ant for ant in ants if ant != self and max(abs(ant.x - self.x), abs(ant.y - self.y)) <= 1]

        # Check for attrition dynamically based on encounters
        if self.state.startswith('committed') and not self.has_food:
            # Interaction with another ant can cause reconsideration
            if nearby_ants and random.random() < (0.1 * len(nearby_ants)):  # 10% per nearby ant
                self.state = 'uncommitted'

        # Interaction with feeders
        for feeder in feeders:
            if (self.x, self.y) == (feeder.x, feeder.y):
                # Ant picks up food if it finds food at a feeder and is not already carrying food
                if feeder.food > 0 and not self.has_food:
                    feeder.food -= 1
                    self.has_food = True
                    # Immediate commitment to the feeder where it picks up the food
                    self.state = 'committed_A' if feeder == feeders[0] else 'committed_B'
                # When ant has food and reaches the nest, it deposits the food
                elif self.has_food and (self.x, self.y) == NEST:
                    self.has_food = False  # Ant drops off food
                    # Strong chance to become uncommitted after food delivery
                    if random.random() < 0.8:  # 80% chance to become uncommitted
                        self.state = 'uncommitted'

        # Recruitment interaction only if ant is committed and has food
        if self.state.startswith('committed') and self.has_food:
            for ant in nearby_ants:
                if ant.state == 'uncommitted':
                    recruitment_chance = 0.5  # Flat 50% chance to recruit
                    if random.random() < recruitment_chance:
                        ant.state = self.state  # Recruit to the same state






class Feeder:
    def __init__(self, x, y, food):
        self.x = x
        self.y = y
        self.food = food

class Simulation:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.ants = [Ant(NEST[0], NEST[1]) for _ in range(NUM_ANTS)]
        self.feeders = [Feeder(FEEDER_A[0], FEEDER_A[1], INITIAL_FOOD), Feeder(FEEDER_B[0], FEEDER_B[1], INITIAL_FOOD)]
        self.ant_count_A = []
        self.ant_count_B = []
        self.uncommitted_ants = []
        self.food_A = [INITIAL_FOOD]
        self.food_B = [INITIAL_FOOD]

    def run_step(self):
        count_A = count_B = count_uncommitted = 0
        for ant in self.ants:
            ant.move()
            ant.update_state(self.feeders, self.ants)
            # Count states for plotting
            if ant.state == 'committed_A':
                count_A += 1
            elif ant.state == 'committed_B':
                count_B += 1
            else:
                count_uncommitted += 1

        # Append counts for plotting
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
        param_log = open(os.path.join(self.folder_name, 'context.txt'), 'w')
        param_log.write(f"NUM_ANTS = {NUM_ANTS}\nINITIAL_FOOD = {INITIAL_FOOD}\n"
                        f"ALPHA_A = {ALPHA_A}\nALPHA_B = {ALPHA_B}\n"
                        f"BETA_A = {BETA_A}\nBETA_B = {BETA_B}\n"
                        f"LAMBDA_A = {LAMBDA_A}\nLAMBDA_B = {LAMBDA_B}\n"
                        f"Feeder A: {FEEDER_A}\nFeeder B: {FEEDER_B}\n"
                        f"Timesteps: {timesteps}")
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
    folder_name = find_available_folder()  # Get the folder name first
    sim = Simulation(folder_name)  # Pass the folder name to the Simulation
    for step in range(timesteps):  # Simulate for 1000 time steps
        sim.run_step()
        if step % 50 == 0:  # Update grid plot every 50 steps
            sim.plot_grid(step)

    # Plot the final state of the grid
    sim.plot_results()

if __name__ == "__main__":
    main()