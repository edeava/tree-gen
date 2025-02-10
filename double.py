import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

class DualCellularAutomata:
    def __init__(self, size=50):
        # 0 = empty, 1 = type A, 2 = type B
        self.grid = np.random.choice([0, 1, 2], size=(size, size), p=[0.8, 0.1, 0.1])
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        
        # Create custom colormap
        self.cmap = mcolors.ListedColormap(['white', 'green', 'brown'])
        self.bounds = [-0.5, 0.5, 1.5, 2.5]
        self.norm = mcolors.BoundaryNorm(self.bounds, self.cmap.N)
        
    def count_neighbors(self, i, j, cell_type):
        total = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni = (i + di) % self.grid.shape[0]
                nj = (j + dj) % self.grid.shape[1]
                if self.grid[ni, nj] == cell_type:
                    total += 1
        return total

    def update(self):
        self.ax.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Display current state with proper colormap
        img = self.ax.imshow(self.grid, cmap=self.cmap, norm=self.norm)
        
        new_grid = self.grid.copy()
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                type_a_neighbors = self.count_neighbors(i, j, 1)
                type_b_neighbors = self.count_neighbors(i, j, 2)
                
                current = self.grid[i, j]
                
                if current == 0:  # Empty cell
                    # Type A birth: needs exactly 3 type A neighbors
                    if type_a_neighbors == 3 and type_b_neighbors < 2:
                        new_grid[i, j] = 1
                    # Type B birth: needs 2-3 type B neighbors and no type A neighbors
                    elif type_b_neighbors in [2, 3] and type_a_neighbors == 0:
                        new_grid[i, j] = 2
                
                elif current == 1:  # Type A cell
                    if i % 2 != 0:
                        break
                    # Type A survival: needs 2-3 neighbors, dies if too many type B nearby
                    if type_a_neighbors not in [2, 3] or type_b_neighbors > 2:
                        new_grid[i, j] = 0
                
                else:  # Type B cell
                    # Type B survival: needs 1-4 type B neighbors, no type A influence
                    if type_b_neighbors < 1 or type_b_neighbors > 4:
                        new_grid[i, j] = 0
                        
        self.grid = new_grid
        return img

    def animate(self):
        anim = FuncAnimation(self.fig, self.update, frames=200, interval=100)
        plt.show()

# Create and run the simulation
game = DualCellularAutomata()
game.animate()