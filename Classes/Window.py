import pygame
from sys import exit
import math
import os

import random
pygame.display.init()
pygame.font.init()

#******************************************************* CONSTANTS *******************************************************

#SCREEN
X_SCRNSIZE, Y_SCRNSIZE = 1200, 800
SCREEN = pygame.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))

#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
PURPLE = ( 211, 3, 252)
YELLOW = (255, 241, 0)


class Window:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = BLACK
        self.paused = 0
        


    def display(self):
        SCREEN.fill(self.color)
        pygame.display.set_caption("Asteroids")

    def title_screen(self):
        ASTEROIDS_TITLE_FONT = pygame.font.SysFont('keyboard', 150)
        ASTEROIDS_TITLE_TEXT = "ASTEROIDS"
        draw_text_ast = ASTEROIDS_TITLE_FONT.render(ASTEROIDS_TITLE_TEXT, 1, WHITE)
        SCREEN.blit(draw_text_ast, (X_SCRNSIZE/2 - draw_text_ast.get_width() / 2, Y_SCRNSIZE/2 - draw_text_ast.get_height() / 2 - 40))
        
    def signature(self):
        
        #font if ran from PythonProjects folder
        SIGNATURE_FONT = pygame.font.Font(os.path.join('/Users','jeremyzay','Desktop','PythonProjects','Asteroids II', 'Assets', 'Fonts', 'Font2.otf'), 50)

        #font if ran from Asteroids folder
        #SIGNATURE_FONT = pygame.font.Font(os.path.join('Fonts', 'Font2.otf'), 50)
        
        SIGNATURE_TEXT = "Jeremy Zay"
        draw_text_ast = SIGNATURE_FONT.render(SIGNATURE_TEXT, 1, WHITE)
        SCREEN.blit(draw_text_ast, (X_SCRNSIZE/2 - draw_text_ast.get_width() / 2, Y_SCRNSIZE - draw_text_ast.get_height() / 2 - 120))
        
        
    def pause(self):
        
        PAUSE_FONT1 = pygame.font.SysFont('keyboard', 40)
        
        PAUSE_TEXT1 = "P A U S E D"
        
        text1_height = 20
        

        #PAUSED
        pause_text1 = PAUSE_FONT1.render(PAUSE_TEXT1, 1, WHITE)
        SCREEN.blit(pause_text1, (X_SCRNSIZE/2 - pause_text1.get_width() / 2, pause_text1.get_height() / 2  + text1_height))

    def display_debug_value(self, value, coords):
        FONT = pygame.font.SysFont('keyboard', 40)
        TEXT = str(value)
        text_var = FONT.render(TEXT, 1, WHITE)
        SCREEN.blit(text_var, coords)
