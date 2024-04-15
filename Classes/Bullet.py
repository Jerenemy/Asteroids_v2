import pygame
from sys import exit
import math
import random
pygame.display.init()
pygame.font.init()


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

#******************************************************* CLASSES *******************************************************


# Class Bullet **********************************************  
class Bullet:
    def __init__(self, space_ship, bullet_speed, fire_direction, bullet_source):
            self.color = WHITE
            #self.x_coord = space_ship.x_coord
            #self.y_coord = space_ship.y_coord
            self.size = 3
            self.speed = bullet_speed
            self.direction = fire_direction
            self.hit = 0
            self.hit_points = 0
            self.x_coord = space_ship.x_coord + ((space_ship.size + space_ship.speed + self.speed ) * math.cos(math.pi / 180 * (fire_direction - 90) ))
            self.y_coord = space_ship.y_coord + ((space_ship.size + space_ship.speed + self.speed ) * math.sin(math.pi / 180 * (fire_direction - 90) ))
            self.bullet_source = bullet_source
            

    #Method move in Class Bullet - move bullet
    def move(self): 
        self.x_coord = self.x_coord + (self.speed * math.cos(math.pi / 180 * (self.direction - 90) ))
        self.y_coord = self.y_coord + (self.speed * math.sin(math.pi / 180 * (self.direction - 90) ))
        
        if self.x_coord < (0 - self.size) or self.x_coord > (X_SCRNSIZE + self.size) or self.y_coord < (0 - self.size) or  self.y_coord > (Y_SCRNSIZE + self.size): 
            self.speed = 0

    #Method display in Class Bullet - display bullet
    def display(self):
        pygame.draw.circle(SCREEN, self.color, [self.x_coord, self.y_coord], self.size)

    #Method check_distance in Class Bullet - check asteroids distance against bullets    
    def check_distance(self, space_object_list):       
        i = 0
        while i < len(space_object_list):   
            d = math.sqrt(((space_object_list[i].x_coord - self.x_coord) ** 2) + ((space_object_list[i].y_coord - self.y_coord) ** 2) )
            if d < space_object_list[i].size + self.size:
                #mark bullet as hit or spent
                self.hit = 1
                self.speed = 0
                return(space_object_list[i].points)            
            i = i + 1
        return(0)

    def generate_random_direction(self):
        self.color = RED
        self.direction = random.randrange(45, 315, 90)

