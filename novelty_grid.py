import math
import sys

import numpy as np
import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 50
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Game")
clock = pygame.time.Clock()

# Grid initialization
grid = np.full((GRID_SIZE, GRID_SIZE), False, dtype=bool)


def draw_grid():
    """Draws the grid"""
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = BLACK if grid[y][x] else WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def set_cell(x, y, value: bool):
    """Enables / disables a cell"""
    grid[y // CELL_SIZE][x // CELL_SIZE] = value


def get_neighbours(x, y):
    """Get all neighbours for a cell. Neighbours are horizontally / vertically adjacent cells."""
    neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for n_x, n_y in neighbours:
        if n_x >= GRID_SIZE or n_y >= GRID_SIZE or n_x < 0 or n_y < 0:
            # Skip cells which are outside the canvas
            neighbours.remove((n_x, n_y))

    return neighbours


def euclidean_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def furthest_cell(active_cells, neighbours):
    """Find the one neighbour cell which is furthest away from all existing cells"""
    distances = []
    for neighbour in neighbours:
        total_distance = 0
        for cell in active_cells:
            total_distance += euclidean_distance(neighbour, cell)
        distances.append(total_distance)

    furthest_neighbour_index = distances.index(max(distances))
    return neighbours[furthest_neighbour_index]


def enable_furthest_cell():
    # Get existing cells
    active_cells = np.argwhere(grid)

    # Collect all neighbours
    neighbours = []
    for current_x, current_y in active_cells:
        # Get all adjacent cells
        for neighbour_x, neighbour_y in get_neighbours(current_x, current_y):
            # Consider only disabled cells
            if not grid[neighbour_x, neighbour_y]:
                neighbours.append((neighbour_x, neighbour_y))

    furthest = furthest_cell(active_cells, neighbours)
    grid[furthest[0], furthest[1]] = True


# Main loop
program_running = True
growing = False
while program_running:
    # Controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button -> draw
                set_cell(*pygame.mouse.get_pos(), True)
            elif pygame.mouse.get_pressed()[2]:  # Right mouse button -> erase
                set_cell(*pygame.mouse.get_pos(), False)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                growing = not growing

    # Growing animation
    if growing:
        enable_furthest_cell()

    draw_grid()

    pygame.display.flip()
    clock.tick(24)

pygame.quit()
sys.exit()
