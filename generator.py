import pygame
import random


DELAY = 10

class Cell:
    def __init__(self, row, column, width, height, color=(150, 150, 150)):
        self.color = color
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.is_visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        
        self.g_score = None
        self.h_score = None

    def draw(self, screen, cell_size, start_pos, font):
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

        if self.g_score is not None and self.h_score is not None:
            f_score_text = font.render(f"{self.g_score} + {self.h_score}", True, (0, 0, 0))
            screen.blit(f_score_text, (x + cell_size // 6, y + cell_size // 4))


class Maze:
    def __init__(self, screen_size, screen, cell_size=50, padding=20):
        self.screen_size = screen_size
        self.screen = screen
        self.cell_size = cell_size
        self.padding = padding
        self.rows = (screen_size[1] - 2 * padding) // cell_size
        self.columns = (screen_size[0] - 2 * padding) // cell_size
        self.grid = [[Cell(row, column, self.cell_size, self.cell_size) for column in range(self.columns)] for row in range(self.rows)]
        self.font = pygame.font.SysFont('Arial', 12, bold=True)

    def draw(self):
        self.start_position = ((((self.screen_size[0] - (self.padding * 2)) % self.cell_size) / 2 + self.padding),
                        (((self.screen_size[1] - (self.padding * 2)) % self.cell_size) / 2 + self.padding))

        self.screen.fill((21, 21, 21))

        for row in self.grid:
            for cell in row:
                cell.draw(self.screen, self.cell_size, self.start_position, self.font)

    def update_screen(self, delay=0):
        self.draw()
        pygame.display.flip()
        if delay:
            pygame.time.delay(delay)

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
                self.update_screen(DELAY // 2)
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
