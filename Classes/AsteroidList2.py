import pygame
from sys import exit
import math
import random
from Classes.Spaceship4 import Spaceship
pygame.display.init()
pygame.font.init()
from Classes.Asteroid2 import Asteroid
import os

#******************************************************* CONSTANTS *******************************************************

#SCREEN
X_SCRNSIZE, Y_SCRNSIZE = 1200, 800
SCREEN = pygame.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))

FPS = 50

#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
PURPLE = ( 211, 3, 252)
YELLOW = (255, 241, 0)

#SPACESHIP MOVEMENT
ACCELERATION = 0.3
DECELERATION = 0.02
ROTATE = 5

RAD2DEG = 180 / math.pi
DEG2RAD = math.pi / 180

#******************************************************* SOUNDS *******************************************************



"""bang_ast_destroy = pygame.mixer.Sound(os.path.join('Asteroids', 'AsteroidSounds', 'bangLarge.wav'))

bang_ast_destroy = pygame.mixer.Sound(os.path.join('AsteroidSounds', 'bangLarge.wav'))
"""

#******************************************************* CLASSES *******************************************************

#Class AsteroidList - list of Asteroids ******************************************
class AsteroidList(list):
    def __init__(self):
        self.asteroid_destroy_sound_play = 0


    #Method move_asteroids in Class AsteroidList:
    def move_asteroids(self):       
        i = 0
        while i < len(self):   
            self[i].move()
            if self[i].x_coord < (0 - self[i].size) or self[i].x_coord > (X_SCRNSIZE + self[i].size) or self[i].y_coord < (0 - self[i].size) or  self[i].y_coord > (Y_SCRNSIZE + self[i].size): 
                self.pop(i)            
            i = i + 1

    #Method check_asteroids in Class AsteroidList:
    def check_if_asteroids_hit(self, bullet_list):       
        i = 0
        while i < len(self):   
            hit = self[i].check_distance(bullet_list)
            self[i].hit = hit
            i = i + 1
            

    

    #Method display_asteroids in Class AsteroidList:
    def display_asteroids(self, SCREEN):        
        i = 0
        while i < len(self):   
            self[i].display(SCREEN)
            i = i + 1

    def split_asteroids(self):
        i = 0 
        while i < len(self):
            random_direction_change1 = random.randrange(-60,60,30)
            random_direction_change2 = random.randrange(-60,60,30)

            if self[i].hit == 1 and self[i].size > 30:
                if random_direction_change1 != random_direction_change2:
                    
                    #(-1/8) * self[i].size/2 + 7
                    new_asteroid1 = Asteroid(self[i].color, self[i].x_coord, self[i].y_coord, self[i].size/2, self[i].speed , self[i].direction + random_direction_change1)
                    new_asteroid2 = Asteroid(self[i].color, self[i].x_coord, self[i].y_coord, self[i].size/2, self[i].speed, self[i].direction + random_direction_change2)
                    self.append(new_asteroid1)
                    self.append(new_asteroid2)
                else:
                    #(-1/8) * self[i].size/2 + 7
                    new_asteroid1 = Asteroid(self[i].color, self[i].x_coord, self[i].y_coord, self[i].size/2, self[i].speed , self[i].direction + 45)
                    new_asteroid2 = Asteroid(self[i].color, self[i].x_coord, self[i].y_coord, self[i].size/2, self[i].speed, self[i].direction - 45)
                    self.append(new_asteroid1)
                    self.append(new_asteroid2)
                    
                    #new_asteroid.append(SCREEN, self.color, self.x_coord, self.y_coord, self.size/2, self.speed, self.direction + 45)
            i = i + 1
            
            #if spaceship hits
            ("""or sship.check_distance(self) != 0""")

    def delete_hit_asteroids(self):       
        i = 0
        while i < len(self):   
            if self[i].hit == 1:
                
                self.asteroid_destroy_sound_play = 1
                
                self.pop(i)            
            i = i + 1

    """def refresh_screen_asteroids(self):
        i = 0
        while i < len(self):  
            self.clear()
        i = i + 1"""

