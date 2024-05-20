import pygame # type: ignore
import sys
import random
from util import StackFrontier, QueueFrontier, Node


DELAY = 120

class Cell:
    def __init__(self, row, column, width, height, color=(150, 150, 150)):
        self.color = color
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.is_visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def draw(self, screen, cell_size, start_pos):
        x = self.column * cell_size + start_pos[0]
        y = self.row * cell_size + start_pos[1]

        line_color = pygame.Color(238, 247, 255)

        pygame.draw.rect(screen, self.color, (x, y, cell_size, cell_size))

        if self.walls["top"]:
            pygame.draw.line(screen, line_color, (x, y), (x + cell_size, y), 4)
        if self.walls["right"]:
            pygame.draw.line(screen, line_color, (x + cell_size, y), (x + cell_size, y + cell_size), 4)
        if self.walls["bottom"]:
            pygame.draw.line(screen, line_color, (x, y + cell_size), (x + cell_size, y + cell_size), 4)
        if self.walls["left"]:
            pygame.draw.line(screen, line_color, (x, y), (x, y + cell_size), 4)


class Maze:
    def __init__(self, screen_size, screen, cell_size=50, padding=20):
        self.screen_size = screen_size
        self.screen = screen
        self.cell_size = cell_size
        self.padding = padding
        self.rows = (screen_size[1] - 2 * padding) // cell_size
        self.columns = (screen_size[0] - 2 * padding) // cell_size
        self.grid = [[Cell(row, column, self.cell_size, self.cell_size) for column in range(self.columns)] for row in range(self.rows)]

    def draw(self):
        self.start_position = ((((self.screen_size[0] - (self.padding * 2)) % self.cell_size) / 2 + self.padding),
                        (((self.screen_size[1] - (self.padding * 2)) % self.cell_size) / 2 + self.padding))

        self.screen.fill((21, 21, 21))

        for row in self.grid:
            for cell in row:
                cell.draw(self.screen, self.cell_size, self.start_position)
    
    def generate_maze(self):
        start_cell = self.grid[0][0]
        self._dfs(start_cell)

    def _dfs(self, current_cell):
        current_cell.is_visited = True
        neighbors = self._get_unvisited_neighbors(current_cell)
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if not neighbor.is_visited:
                self._remove_walls(current_cell, neighbor)
                # Updates screen for each dfs move
                self.draw()
                pygame.display.flip()
                pygame.time.delay(DELAY // 6)
                self._dfs(neighbor)

    def _get_unvisited_neighbors(self, cell):
        neighbors = []
        row, column = cell.row, cell.column
        if row > 0 and not self.grid[row - 1][column].is_visited:
            neighbors.append(self.grid[row - 1][column])
        if row < self.rows - 1 and not self.grid[row + 1][column].is_visited:
            neighbors.append(self.grid[row + 1][column])
        if column > 0 and not self.grid[row][column - 1].is_visited:
            neighbors.append(self.grid[row][column - 1])
        if column < self.columns - 1 and not self.grid[row][column + 1].is_visited:
            neighbors.append(self.grid[row][column + 1])
        return neighbors

    def _remove_walls(self, cell1, cell2):
        if cell1.row == cell2.row:
            if cell1.column < cell2.column:
                cell1.walls['right'] = False
                cell2.walls['left'] = False
            else:
                cell1.walls['left'] = False
                cell2.walls['right'] = False
        elif cell1.column == cell2.column:
            if cell1.row < cell2.row:
                cell1.walls['bottom'] = False
                cell2.walls['top'] = False
            else:
                cell1.walls['top'] = False
                cell2.walls['bottom'] = False


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
                return None
            
            neighbors = self._neighbors(node.state)

            if neighbors:
                for neighbor in neighbors:
                    if neighbor[0] not in explored and not frontier.contains_state(neighbor[0]):
                        child = Node(state=neighbor[0], parent=node, action=neighbor[1])
                        frontier.add(child, neighbor[0])

            explored.add(node.state)
            for cell in explored:
                cell.color = (255, 100, 100)
                
            self.maze.draw()
            pygame.display.flip()
            pygame.time.delay(DELAY * 2)

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
                self.goal.color = (100, 255, 100)
                return None
            
            neighbors = self._neighbors(node.state)

            if neighbors:
                for neighbor in neighbors:
                    if neighbor[0] not in explored and not frontier.contains_state(neighbor[0]):
                        child = Node(state=neighbor[0], parent=node, action=neighbor[1])
                        frontier.add(child, neighbor[0])

            explored.add(node.state)
            for cell in explored:
                cell.color = (255, 100, 100)
                
            self.maze.draw()
            pygame.display.flip()
            pygame.time.delay(DELAY)

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


if __name__ == "__main__":
    pygame.init()

    #size = (random.randint(600, 1600), random.randint(300, 900))
    size = (1000, 1000)
    screen = pygame.display.set_mode(size)
    maze = Maze(size, screen)
    maze.generate_maze()
    solver = MazeSolver(maze=maze, start=maze.grid[0][0], goal=maze.grid[-1][-1])
    solver.solve()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
