from maze_solver import MazeSolver
from generator import Maze
import pygame
import random
import sys


def main():
    pygame.init()
    pygame.display.set_caption("Path Finder")

    size = (random.randint(600, 1300), random.randint(300, 700))
    screen = pygame.display.set_mode(size)

    maze = Maze(size, screen)
    maze.generate_maze()

    solver = MazeSolver(maze=maze, start=maze.grid[0][0], goal=maze.grid[-1][-1])
    solver.solve()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    main()
