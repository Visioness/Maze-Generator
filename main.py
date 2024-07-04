from maze_solver import MazeSolver
from generator import Maze
import pygame
import random
import sys


def main():
    pygame.init()
    pygame.display.set_caption("Path Finder")

    size = (random.randint(1000, 1600), random.randint(700, 900))
    screen = pygame.display.set_mode(size)

    maze = Maze(size, screen)
    maze.generate_maze()
    
    start = maze.grid[random.randint(1, maze.rows - 1)][random.randint(1, maze.columns - 1)]
    goal = maze.grid[random.randint(1, maze.rows - 1)][random.randint(1, maze.columns - 1)]

    solver = MazeSolver(
        maze=maze, 
        start=start,
        goal=goal
    )
    solver.solve()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
