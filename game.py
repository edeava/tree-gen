import pygame
import numpy as np

from energy import EnergyCellularAutomata

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 5
WIDTH = 800
HEIGHT = WIDTH
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cellular Automata")

game = EnergyCellularAutomata(COLS)
print(game.get_color_array().shape)
# Initialize grid randomly

def draw_from_colors(colorArray):
    # Convert the color array to a surface
    surface = pygame.surfarray.make_surface(colorArray)
    # Scale it up to the window size
    scaled_surface = pygame.transform.scale(surface, (WIDTH, HEIGHT))
    # Draw it to the screen
    screen.blit(scaled_surface, (0, 0))

# Game loop
running = True
start = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Add mouse interaction to toggle cells
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start = False
            pos = pygame.mouse.get_pos()
            print(pos[1] // CELL_SIZE, pos[0] // CELL_SIZE)
            for i in range(-10, 10):
                for j in range(-10, 10):
                    col = (pos[1] + i) // CELL_SIZE
                    row = (pos[0] + j) // CELL_SIZE
                    game.grid[row, col] = not game.grid[row, col]
                    game.energy[row, col] = 80 * game.grid[row, col]
        elif event.type == pygame.MOUSEBUTTONUP:
            start = True
    if start:
        game.update()
    
    draw_from_colors(game.get_color_array())
    pygame.display.flip()
    pygame.time.wait(10)  # Control animation speed

pygame.quit()