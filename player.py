# This file was created by: Bradley Kemp
# Sources: https://thepythoncode.com/article/build-a-maze-game-in-python

import pygame
import os

# folders for extracting images
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

class Player:
    def __init__(self, x, y, a, b, c):
        self.x = int(x)
        self.y = int(y)
        # adjust size
        self.player_size = 10
        self.rect = pygame.Rect(self.x, self.y, self.player_size, self.player_size)
        # for the different colors of player
        self.color = (int(a), int(b), int(c))
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        # adjust for speed
        self.speed = 4

    # get current cell position of the player
    def get_current_cell(self, x, y, grid_cells):
        for cell in grid_cells:
            if cell.x == x and cell.y == y:
                return cell

    # stops player to pass through walls
    def check_move(self, tile, grid_cells, thickness):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)
        current_cell_abs_x, current_cell_abs_y = current_cell_x * tile, current_cell_y * tile
        # i.e. if you press left...
        if self.left_pressed:
            # but there is a wall to the left...
            if current_cell.walls['left']:
                if self.x <= current_cell_abs_x + thickness:
                    # do not move left
                    self.left_pressed = False
        if self.right_pressed:
            if current_cell.walls['right']:
                if self.x >= current_cell_abs_x + tile - (self.player_size + thickness):
                    self.right_pressed = False
        if self.up_pressed:
            if current_cell.walls['top']:
                if self.y <= current_cell_abs_y + thickness:
                    self.up_pressed = False
        if self.down_pressed:
            if current_cell.walls['bottom']:
                if self.y >= current_cell_abs_y + tile - (self.player_size + thickness):
                    self.down_pressed = False
                    # player.py

    # drawing player to the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    # updates player position while moving
    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        self.x += self.velX
        self.y += self.velY
        self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)