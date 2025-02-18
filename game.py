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
space = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Add mouse interaction to toggle cells
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos[1] // CELL_SIZE, pos[0] // CELL_SIZE)
            for i in range(-10, 10):
                for j in range(-10, 10):
                    col = (pos[1] + i) // CELL_SIZE
                    row = (pos[0] + j) // CELL_SIZE
                    game.grid[row, col] = not game.grid[row, col]
                    game.energy[row, col] = 80 * game.grid[row, col]
        elif event.type == pygame.KEYDOWN:
            start = not start
            space += 1 
            print('PAUSED')
            # print(game.random_centers)
    if start:
        game.update()
    if space > 0 and not start:
        space = space % 9
        curr_game_center = game.random_centers[space]
        draw_from_colors(game.get_color_array(add_point = curr_game_center))
    else:
        draw_from_colors(game.get_color_array())
    
    pygame.display.flip()
    pygame.time.wait(1)  # Control animation speed

pygame.quit()