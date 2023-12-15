# This file was created by: Bradley Kemp
# Sources: https://thepythoncode.com/article/build-a-maze-game-in-python

import pygame
from cell import Cell

class Maze:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        # thickness of walls
        self.thickness = 4
        self.grid_cells = [Cell(col, row, self.thickness) for row in range(self.rows) for col in range(self.cols)]

    # carve grid cell walls
    def remove_walls(self, current, next):
        dx = current.x - next.x
        # if dx is 1, next cell is to the left
        # left wall of current cell is removed, and right wall of next cell is removed
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        # if dx is -1, next cell is to the right
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        # if dy is 1, next cell is above
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        # if dy is -1, next cell is below
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False

    # generates maze
    def generate_maze(self):
        # sets current_cell as first cell
        current_cell = self.grid_cells[0]
        array = []
        break_count = 1
        while break_count != len(self.grid_cells):
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(self.cols, self.rows, self.grid_cells)
            # detects next cell and marks as visited
            if next_cell:
                next_cell.visited = True
                break_count += 1
                # add current_cell to the array
                array.append(current_cell)
                # removes the walls of the current_cell and its neighbor, creating a pathway
                self.remove_walls(current_cell, next_cell)
                # now, the next_cell becomes the current_cell, continuing the cycle
                current_cell = next_cell
            # if there isn't a next_cell, current_cell comes off of the array
            elif array:
                # backtrack if no neighbors are present in order to have all cells visited, all creating a pathway
                current_cell = array.pop()
        return self.grid_cells