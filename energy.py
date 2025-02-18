import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

class EnergyCellularAutomata:
    def __init__(self, size=180):
        # 0 = empty, 1 = living cell
        # self.grid = np.zeros((5 * (size // 7), size))

        # self.grid = np.concatenate((self.grid, np.random.choice([0, 1], size=(size // 7, size), p=[0.7, 0.3])))

        # self.grid = np.concatenate((self.grid, np.zeros((size - (6 * (size// 7)), size))))
        
        self.grid = np.zeros((size, size))

        self.grid = self.grid.T
        self.center_cores = 9

        self.energy = np.zeros((size, size))
        self.energy[self.grid > 0] = np.random.randint(low=33, high=100)
        self.age = np.zeros((size, size))
        
        self.clouds = np.zeros((size, size))
        self.random_centers = np.random.random_sample(size=(self.center_cores,2)) * size
        self.random_centers = self.random_centers.astype(int, copy=True)
        print(self.random_centers)
        
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                max_sun = 0
                for k in range(self.random_centers.shape[0]):
                    distance = int((i - self.random_centers[k][0]) * (i - self.random_centers[k][0]) +
                                       (j - self.random_centers[k][1]) * (j - self.random_centers[k][1]))
                    norm_distance = np.clip(1 - (distance / (size**1.4)) , 0, 1)
                    max_sun = np.maximum(max_sun, norm_distance)
                self.clouds[i][j] = max_sun

        # Create custom colormap: White -> Green -> Black
        self.colors = [(0,0,0), (0,1,0)]
        self.cmap = mcolors.LinearSegmentedColormap.from_list('energy', self.colors)
        
        # Parameters
        self.energy_decay = 0.1
        self.min_survival_energy = 12
        self.reproduction_energy = 80
        self.energy_transfer_rate = 0.01
        self.sunlight_energy = 1
        self.death_age = 75
        
    def add_environmental_energy(self):
        # height_factor = 1.1 - np.abs(np.geomspace(0.1, 1.1, self.grid.shape[0]))
        # height_factor = height_factor[:, np.newaxis]
        # print(height_factor)
        self.energy = self.sunlight_energy * self.clouds + (self.energy)
        
    def transfer_energy(self, i, j):
        if self.grid[i, j] == 0:
            return 0
            
        total_transfer = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni = (i + di) % self.grid.shape[0]
                nj = (j + dj) % self.grid.shape[1]
                
                if self.grid[ni, nj] > 0:
                    energy_diff = self.energy[i, j] - self.energy[ni, nj]
                    if energy_diff > 0:
                        transfer = self.energy_transfer_rate
                        self.energy[i, j] -= transfer
                        self.energy[ni, nj] += transfer
                        total_transfer += transfer
        return total_transfer

    def get_color_array(self, add_point = []):
        # Normalize energy levels to [0,1] for color mapping
        max_energy = max(self.reproduction_energy * 1.5, self.energy.max())
        norm_energy = np.clip(self.energy / max_energy, 0, 1)
        
        # Create RGB array
        color_array = np.zeros((*self.grid.shape, 3))
        
        # Set colors based on cell state and energy
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i, j] == 0:
                    color_array[i, j] = [0, 0, 0]  # Black for empty cells
                    color_array[i, j] += self.clouds[i, j] * np.array([1.0,1.0,0.0]) # Yellow gradient
                    # print(color_array[i][j])
                else:
                    color_array[i, j] = self.cmap(norm_energy[i, j])[:3]  # Green gradient
                if len(add_point) > 0 and i <= add_point[0] + 3 and  i >= add_point[0] - 3 and j <= add_point[1] + 3 and  j >= add_point[1] - 3:
                    color_array[i, j] = [1, 0, 0]
                
        
        return color_array * 255

    def update(self):
        # self.ax.clear()
        self.add_environmental_energy()
        
        # Display current state with energy-based colors
        # self.ax.imshow(self.get_color_array())
        # self.ax.set_xticks([])
        # self.ax.set_yticks([])
        
        new_grid = self.grid.copy()
        new_energy = self.energy.copy()
        
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i, j] > 0:
                    self.transfer_energy(i, j)
                    new_energy[i, j] -= self.energy_decay
                    self.age[i,j] += 1
                    
                    if new_energy[i, j] < self.min_survival_energy:
                        new_grid[i, j] = 0
                        new_energy[i, j] = 0
                    
                    elif new_energy[i, j] > self.reproduction_energy:
                        for di in [-1, 0, 1]:
                            for dj in [-1, 0, 1]:
                                if di == 0 and dj == 0:
                                    continue
                                ni = (i + di) % self.grid.shape[0]
                                nj = (j + dj) % self.grid.shape[1]
                                if new_grid[ni, nj] == 0:
                                    new_grid[ni, nj] = 1
                                    split_energy = new_energy[i, j] / 2
                                    new_energy[i, j] = split_energy
                                    new_energy[ni, nj] = split_energy
                                    break
                    if self.age[i,j] > self.death_age :
                        new_energy[i,j] = 0
                        new_grid[i,j] = 0
                        self.age[i,j] = 0
                            
        self.grid = new_grid
        self.energy = new_energy

    def animate(self):
        anim = FuncAnimation(self.fig, self.update, frames=200, interval=100)
        plt.show()

# Create and run the simulation
# game = EnergyCellularAutomata()
# game.animate()