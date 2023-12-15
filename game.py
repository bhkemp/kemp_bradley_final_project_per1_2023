# This file was created by: Bradley Kemp
# Sources: https://thepythoncode.com/article/build-a-maze-game-in-python

import pygame

pygame.font.init()
ORANGE = (250, 120, 60)
GREEN = (120, 250, 60)

class Game:
    def __init__(self, goal_cell, tile):
        self.font = pygame.font.SysFont("impact", 25)
        self.message_color = pygame.Color("darkorange")
        self.goal_cell = goal_cell
        self.tile = tile

    # add goal point for player to reach
    def add_goal_point(self, screen):
        # adding gate for the goal point
        img_path = 'final_project/kemp_bradley_final_project_per1_2023/img/gate.png'
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (self.tile, self.tile))
        screen.blit(img, (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile))

    # winning message for player1
    def message1(self):
        self.message_color = pygame.Color(ORANGE)
        msg = self.font.render('Player 1 Wins!', True, self.message_color)
        return msg
    
    # winning message for player2
    def message2(self):
        self.message_color = pygame.Color(GREEN)
        msg = self.font.render('Player 2 Wins!', True, self.message_color)
        return msg

    # checks if player reached the goal point
    def is_game_over(self, player):
        goal_cell_abs_x, goal_cell_abs_y = self.goal_cell.x * self.tile, self.goal_cell.y * self.tile
        if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y:
            return True
        else:
            return False