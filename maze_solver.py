from util import StackFrontier, QueueFrontier, Node
import pygame


DELAY = 120

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
        start_cell = self.start
        self._bfs(start_cell)

    def _dfs(self, start_cell):
        frontier = StackFrontier()
        explored = set()

        root_node = Node(state=start_cell, parent=None, action=None)
        frontier.add(root_node, start_cell)

        while True:
            if frontier.empty():
                return None

            node = frontier.remove()

            if node.state == self.goal:
                # Returns the solution
                self.goal.color = (100, 255, 100)
                self.update_screen()

            neighbors = self._neighbors(node.state)

            if neighbors:
                for neighbor in neighbors:
                    if neighbor[0] not in explored and not frontier.contains_state(neighbor[0]):
                        child = Node(state=neighbor[0], parent=node, action=neighbor[1])
                        frontier.add(child, neighbor[0])

            explored.add(node.state)
            node.state.color = (255, 100, 100)

            self.maze.update_screen(DELAY * 2)

    def _bfs(self, start_cell):
        frontier = QueueFrontier()
        explored = set()

        root_node = Node(state=start_cell, parent=None, action=None)
        frontier.add(root_node, start_cell)

        while True:
            if frontier.empty():
                return None

            node = frontier.remove()

            if node.state == self.goal:
                # Returns the solution
                while node.parent is not None:
                    node.state.color = (100, 255, 100)
                    self.maze.update_screen(DELAY * 2)

                    node = node.parent
                node.state.color = (100, 255, 100)
                self.maze.update_screen()
                break

            neighbors = self._neighbors(node.state)

            if neighbors:
                for neighbor in neighbors:
                    if neighbor[0] not in explored and not frontier.contains_state(neighbor[0]):
                        child = Node(state=neighbor[0], parent=node, action=neighbor[1])
                        frontier.add(child, neighbor[0])

            explored.add(node.state)
            node.state.color = (255, 100, 100)

            self.maze.update_screen(DELAY * 2)

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
