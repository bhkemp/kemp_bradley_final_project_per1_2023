# This file was created by: Bradley Kemp
# Sources:

# Title: Tracker
# Goals: 
# Title screen
# Maze style game involving a runner
# Auto generated maze
# Similar to that of Pacman
# Abilities
# Required to collect certain items
# Enemies spawn in later
# Maze gets more difficult as your progress
# End screen + replay button

# Still brainstorming...

import pygame as pg
from random import choice
from pygame.sprite import Sprite
from pygame.math import Vector2 as vec
import os
from settings import *

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Cell(pg.sprite.Sprite):
    w, h = 16, 16

    def __init__(self, x, y, maze):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface([self.w, self.h])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x * self.w
        self.rect.y = y * self.h

        self.x = x
        self.y = y
        self.maze = maze
        self.nbs = [(x + nx, y + ny) for nx, ny in ((-2, 0), (0, -2), (2, 0), (0, 2))
                    if 0 <= x + nx < maze.w and 0 <= y + ny < maze.h]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # Makes self.game into game for convenience purposes
        self.game = game
        # An image for player
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # Sets attributes, like health and score, but also velocity and acceleration
        self.rect.center = (0, 0)
        self.pos = vec((Cell.w * 41)/2, (Cell.h * 41)/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 3
        self.score = 0
    # Defines the controls, setting different movements to keys
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.direction.x = -5
        if keys[pg.K_d]:
            self.direction.x = 5
        if keys[pg.K_w]:
            self.direction.y = -5
        if keys[pg.K_s]:
            self.direction.y = 5
        else:
            self.direction.x = 0
            self.direction.y = 0


class Wall(Cell):
    def __init__(self, x, y, maze):
        super(Wall, self).__init__(x, y, maze)
        self.image.fill((0, 0, 0))
        self.type = 0


class Maze:
    def __init__(self, size):
        self.w, self.h = size[0] // Cell.w, size[1] // Cell.h
        self.grid = [[Wall(x, y, self) for y in range(self.h)] for x in range(self.w)]

    def get(self, x, y):
        return self.grid[x][y]

    def place_wall(self, x, y):
        self.grid[x][y] = Wall(x, y, self)

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                cell.draw(screen)

    def generate(self, screen=None, animate=False):
        unvisited = [c for r in self.grid for c in r if c.x % 2 and c.y % 2]
        cur = unvisited.pop()
        stack = []

        while unvisited:
            try:
                n = choice([c for c in map(lambda x: self.get(*x), cur.nbs) if c in unvisited])
                stack.append(cur)
                nx, ny = cur.x - (cur.x - n.x) // 2, cur.y - (cur.y - n.y) // 2
                self.grid[nx][ny] = Cell(nx, ny, self)
                self.grid[cur.x][cur.y] = Cell(cur.x, cur.y, self)
                cur = n
                unvisited.remove(n)

                if animate:
                    self.draw(screen)
                    pg.display.update()
                    pg.time.wait(10)
            except IndexError:
                if stack:
                    cur = stack.pop()