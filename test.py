import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GameOfLife:
    def __init__(self, size=50):
        self.grid = np.random.choice([0, 1], size=(size, size), p=[0.85, 0.15])
        self.fig, self.ax = plt.subplots()
        
    def update(self, frame):
        self.ax.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Display current state
        self.ax.imshow(self.grid, cmap='binary')
        
        # Calculate next state
        new_grid = self.grid.copy()
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                # Count live neighbors using toroidal boundary
                total = int((self.grid[i, (j-1)%self.grid.shape[0]] + 
                           self.grid[i, (j+1)%self.grid.shape[0]] + 
                           self.grid[(i-1)%self.grid.shape[0], j] + 
                           self.grid[(i+1)%self.grid.shape[0], j] + 
                           self.grid[(i-1)%self.grid.shape[0], (j-1)%self.grid.shape[0]] + 
                           self.grid[(i-1)%self.grid.shape[0], (j+1)%self.grid.shape[0]] + 
                           self.grid[(i+1)%self.grid.shape[0], (j-1)%self.grid.shape[0]] + 
                           self.grid[(i+1)%self.grid.shape[0], (j+1)%self.grid.shape[0]]))
                
                # Apply Conway's rules
                if self.grid[i, j] == 1:
                    if total < 2 or total > 3:
                        new_grid[i, j] = 0
                else:
                    if total == 3:
                        new_grid[i, j] = 1
                        
        self.grid = new_grid

    def animate(self):
        anim = FuncAnimation(self.fig, self.update, frames=200, interval=100)
        plt.show()

# Create and run the simulation
game = GameOfLife()
game.animate()