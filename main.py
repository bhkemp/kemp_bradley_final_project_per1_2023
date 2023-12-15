# This file was created by: Bradley Kemp
# Sources: https://thepythoncode.com/article/build-a-maze-game-in-python

# Title: Maze Runner
# Goals: 
# Title screen
# Maze style game
# Auto generated maze
# Similar to that of Pacman
# Abilities
# Required to collect certain items
# Enemies spawn in later
# Maze gets more difficult as your progress
# End screen + replay button

# Still brainstorming...

import pygame, sys
from maze import *
from player import *
from game import *
from clock import *

snd_folder = os.path.join(game_folder, 'music')

pygame.init()
pygame.font.init()

class Main():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial bold", 25)
        self.message_color = pygame.Color("white")
        self.running = True
        self.game_over = False
        self.player1_wins = False
        self.player2_wins = False
        self.FPS = pygame.time.Clock()

    # instructions printed to right of screen
    def instructions(self):
        instructions1 = self.font.render('Use', True, self.message_color)
        instructions2 = self.font.render('Player 1:', True, self.message_color)
        instructions3 = self.font.render('ARROW KEYS', True, self.message_color)
        instructions4 = self.font.render('Player 2:', True, self.message_color)
        instructions5 = self.font.render('W A S D', True, self.message_color)
        self.screen.blit(instructions1,(660,300))
        self.screen.blit(instructions2,(640,330))
        self.screen.blit(instructions3,(620,360))
        self.screen.blit(instructions4,(640,390))
        self.screen.blit(instructions5,(640,420))

    # draws all configs; maze, player1, player2, instructions, and time
    def _draw(self, maze, tile, player1, player2, game, clock):
        # draw maze
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]
        # add a goal point to reach
        game.add_goal_point(self.screen)
        # draw every player movement
        player1.draw(self.screen)
        player1.update()
        player2.draw(self.screen)
        player2.update()
        # instructions, clock, winning message
        self.instructions()
        if self.game_over:
            # stop timer once game over
            clock.stop_timer()
            # if a player wins, print a message
            if self.player1_wins:
                self.screen.blit(game.message1(), (610,120))
            if self.player2_wins:
                self.screen.blit(game.message2(), (610,120))           
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (625,200))
        pygame.display.flip()

    # main game loop
    def main(self, frame_size, tile):
        cols, rows = frame_size[0] // tile, frame_size[-1] // tile
        maze = Maze(cols, rows)
        game = Game(maze.grid_cells[-1], tile)
        player1 = Player(tile // 3, tile // 3, 250, 120, 60)
        player2 = Player(tile // 3, tile // 3, 120, 250, 60)
        clock = Clock()
        maze.generate_maze() #important
        clock.start_timer()
        # game music!
        pygame.mixer.music.load(os.path.join(snd_folder, 'game_music.mp3'))
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
        # when running, execute:
        while self.running:
            self.screen.fill("black")
            self.screen.fill(pygame.Color("black"), (603, 0, 752, 752))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # if keys were pressed still
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player1.left_pressed = True
            if keys[pygame.K_RIGHT]:
                player1.right_pressed = True
            if keys[pygame.K_UP]:
                player1.up_pressed = True
            if keys[pygame.K_DOWN]:
                player1.down_pressed = True
            if keys[pygame.K_a]:
                player2.left_pressed = True
            if keys[pygame.K_d]:
                player2.right_pressed = True
            if keys[pygame.K_w]:
                player2.up_pressed = True
            if keys[pygame.K_s]:
                player2.down_pressed = True
            player1.check_move(tile, maze.grid_cells, maze.thickness)
            player2.check_move(tile, maze.grid_cells, maze.thickness)
            if not keys[pygame.K_LEFT]:
                player1.left_pressed = False
            if not keys[pygame.K_RIGHT]:
                player1.right_pressed = False
            if not keys[pygame.K_UP]:
                player1.up_pressed = False
            if not keys[pygame.K_DOWN]:
                player1.down_pressed = False
            if not keys[pygame.K_a]:
                player2.left_pressed = False
            if not keys[pygame.K_d]:
                player2.right_pressed = False
            if not keys[pygame.K_w]:
                player2.up_pressed = False
            if not keys[pygame.K_s]:
                player2.down_pressed = False
            player1.check_move(tile, maze.grid_cells, maze.thickness)
            player2.check_move(tile, maze.grid_cells, maze.thickness)
            if game.is_game_over(player1):
                self.game_over = True
                player1.left_pressed = False
                player1.right_pressed = False
                player1.up_pressed = False
                player1.down_pressed = False
                if not self.player2_wins:
                    self.player1_wins = True
            if game.is_game_over(player2):
                self.game_over = True
                player2.left_pressed = False
                player2.right_pressed = False
                player2.up_pressed = False
                player2.down_pressed = False
                if not self.player1_wins:
                    self.player2_wins = True
            self._draw(maze, tile, player1, player2, game, clock)
            self.FPS.tick(60)

if __name__ == "__main__":
    window_size = (602, 602)
    screen = (window_size[0] + 150, window_size[-1])
    # adjust to make maze simpler/harder; increasing size makes it easier
    tile_size = 30
    screen = pygame.display.set_mode(screen)
    pygame.display.set_caption("Maze Runner")

    game = Main(screen)
    game.main(window_size, tile_size) 