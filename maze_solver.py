from util import StackFrontier, QueueFrontier, Node
import pygame
import math
import sys


DELAY = 100
GREEN = (72, 186, 70)
RED = (169, 29, 58)
YELLOW = (240, 160, 65)
BLUE = (50, 84, 226)

class MazeSolver():
    """
    Frontier

    Explored set

    Root node to the Frontier

    Repeat:
        - If empty frontier, stop no solution
        - Remove a node from the frontier, chosen node
        - If goal.state equals to node.state, return the solution
        - Else find new nodes that could be reached from this node, and adds resulting nodes to the frontier
        - Add node to the explored
    """
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal

    def solve(self):
        self.start.color = RED
        self.goal.color = BLUE

        self.maze.update_screen(1500)

        self._astar()

    def _dfs(self):
        frontier = StackFrontier()
        explored = set()

        root_node = Node(state=self.start, parent=None, action=None)
        frontier.add(root_node, self.start)

        while True:
            if frontier.empty():
                return None

            node = frontier.remove()

            if node.state == self.goal:
                # Returns the solution
                while node.parent is not None:
                    if node.state != self.goal:
                        node.state.color = GREEN
                    self.maze.update_screen(DELAY)

                    node = node.parent
                        
                self.maze.update_screen()
                break
                        
            neighbors = self._neighbors(node.state)

            if neighbors:
                for neighbor in neighbors:
                    if neighbor[0] not in explored and not frontier.contains_state(neighbor[0]):
                        child = Node(state=neighbor[0], parent=node, action=neighbor[1])
                        frontier.add(child, neighbor[0])

            explored.add(node.state)
            if node.state != self.start:
                node.state.color = YELLOW

            self.maze.update_screen(DELAY)

    def _bfs(self):
        frontier = QueueFrontier()
        explored = set()

        root_node = Node(state=self.start, parent=None, action=None)
        frontier.add(root_node, self.start)

        while True:
            if frontier.empty():
                return None

            node = frontier.remove()

            if node.state == self.goal:
                # Returns the solution
                while node.parent is not None:
                    if node.state != self.goal:
                        node.state.color = GREEN
                    self.maze.update_screen(DELAY)

                    node = node.parent
        
                self.maze.update_screen()
                break

            neighbors = self._neighbors(node.state)

            if neighbors:
                for neighbor in neighbors:
                    if neighbor[0] not in explored and not frontier.contains_state(neighbor[0]):
                        child = Node(state=neighbor[0], parent=node, action=neighbor[1])
                        frontier.add(child, neighbor[0])

            explored.add(node.state)
            if node.state != self.start:
                node.state.color = YELLOW

            self.maze.update_screen(DELAY)

    def _astar(self):
        frontier = set()
        explored = set()

        
        root_node = Node(state=self.start, parent=None, action=None)
        root_node.state.g_score = 0

        frontier.add((self._calculate_fscore(0, root_node), root_node))

        while True:
            if frontier is None:
                return None

            lowest_fscore = math.inf

            for element in frontier:
                if element[0] < lowest_fscore:
                    lowest_fscore = element[0]
                    node = element[1]
            
            frontier.remove((lowest_fscore, node))
            
            if node.state == self.goal:
                # Returns the solution
                while node.parent is not None:
                    if node.state != self.goal:
                        node.state.color = GREEN
                    self.maze.update_screen(DELAY)

                    node = node.parent
        
                self.maze.update_screen()
                break
            
            neighbors = self._neighbors(node.state)

            if neighbors:
                for neighbor in neighbors:
                    if neighbor[0] not in explored and neighbor[0] not in [element[1].state for element in frontier]:
                        child = Node(state=neighbor[0], parent=node, action=neighbor[1])
                        
                        child.state.g_score = node.state.g_score + 1
                        child.state.h_score = self._calculate_hscore(child)

                        frontier.add((child.state.g_score + child.state.h_score, child))

            explored.add(node.state)
            if node.state != self.start:
                node.state.color = YELLOW

            self.maze.update_screen()
            self._wait_for_space()

    def _neighbors(self, cell):
        neighbors = set()
        if not cell.walls["top"]:
            neighbors.add((self.maze.grid[cell.row - 1][cell.column], "top"))

        if not cell.walls["right"]:
            neighbors.add((self.maze.grid[cell.row][cell.column + 1], "right"))

        if not cell.walls["bottom"]:
            neighbors.add((self.maze.grid[cell.row + 1][cell.column], "bottom"))

        if not cell.walls["left"]:
            neighbors.add((self.maze.grid[cell.row][cell.column - 1], "left"))

        return neighbors if neighbors else None
    
    def _calculate_fscore(self, g_score, node):
        return g_score + self._calculate_hscore(node)

    def _calculate_hscore(self, node):
        return abs(self.goal.row - node.state.row) + abs(self.goal.column - node.state.column)
    
    def _wait_for_space(self):
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if keys[pygame.K_SPACE]:
                pygame.time.delay(200)
                break
            pygame.time.delay(200)