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
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)

#SPACESHIP MOVEMENT
ACCELERATION = 0.3
DECELERATION = 0.02
ROTATE = 5

RAD2DEG = 180 / math.pi
DEG2RAD = math.pi / 180

#*******************************************CLASSES*******************************************

#Class Asteroid *******************************************
class Asteroid:
    def __init__(self, color, x_coord, y_coord, size, speed, direction):
        self.color = color
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.size = size
        self.speed = -0.0375 * self.size + 4.75 #needs updated formula
        self.direction = direction
        self.hit = 0
        rand_min = 50
        rand_max = 150
        rand_inc = 10
        self.r1 = random.randrange(rand_min, rand_max, rand_inc) / 100
        self.r2 = random.randrange(rand_min, rand_max, rand_inc) / 100
        self.r3 = random.randrange(rand_min, rand_max, rand_inc) / 100
        self.r4 = random.randrange(rand_min, rand_max, rand_inc) / 100
        self.r5 = random.randrange(rand_min, rand_max, rand_inc) / 100
        self.r6 = random.randrange(rand_min, rand_max, rand_inc) / 100
        self.r7 = random.randrange(rand_min, rand_max, rand_inc) / 100
        self.r8 = random.randrange(rand_min, rand_max, rand_inc) / 100
        self.width = 3
        
        #self.points_split = 

        if size > 30: 
            self.points = 10
        else: 
            self.points = 100
        
    
    #Method generate_random in Class Asteroid - 
    def generate_random(self):
        random_num = random.randrange(1, 5, 1)
        random_size = random.randrange(20,110,20)
        
        #random_size = random.randrange(30, 50, 5)

        
        if random_num == 1: 
            self.color = BLUE
            self.x_coord = random.randrange(1, X_SCRNSIZE, 1)
            self.y_coord = -40
            self.size = random_size
            self.direction = random.randrange(90, 180,1)
            
        if random_num == 2: 
            self.color = ORANGE
            self.x_coord = X_SCRNSIZE + 40
            self.y_coord = random.randrange(1, Y_SCRNSIZE, 1)
            self.size = random_size
            self.direction = random.randrange(180, 360,1)
           
        if random_num == 3: 
            self.color = PURPLE
            self.x_coord = random.randrange(1, X_SCRNSIZE, 1)
            self.y_coord = Y_SCRNSIZE + 40
            self.size = random_size
            self.direction = random.randrange(270, 450,1)
            
        if random_num == 4: 
            self.color = GREEN
            self.x_coord = -40
            self.y_coord = random.randrange(1, Y_SCRNSIZE, 1)
            self.size = random_size
            self.direction = random.randrange(0, 180,1)
            
        
        if self.size > 30: 
            self.points = 10
        else: 
            self.points = 100
        
        self.speed = -0.0375 * self.size + 5.75
        


    #Method move in Class Asteroid - 
    def move(self):
        self.x_coord = self.x_coord + (self.speed * math.cos(math.pi / 180 * (self.direction - 90) ))
        self.y_coord = self.y_coord + (self.speed * math.sin(math.pi / 180 * (self.direction - 90) ))    

    #Method display in Class Asteroid - def display_asteroid
    def display(self, SCREEN): 
        #rand_size = random.randrange(30, 50, 5)
        
        angle = 0
        angle_inc = 45
        
        
        x1 = self.x_coord + ((self.size * self.r1) * math.cos(math.pi / 180 * angle ))
        y1 = self.y_coord + ((self.size * self.r1) * math.sin(math.pi / 180 * angle ))
        angle = angle + angle_inc
        x2 = self.x_coord + ((self.size * self.r2) * math.cos(math.pi / 180 * angle ))
        y2 = self.y_coord + ((self.size * self.r2) * math.sin(math.pi / 180 * angle ))
        angle = angle + angle_inc
        x3 = self.x_coord + ((self.size * self.r3) * math.cos(math.pi / 180 * angle ))
        y3 = self.y_coord + ((self.size * self.r3) * math.sin(math.pi / 180 * angle ))
        angle = angle + angle_inc
        x4 = self.x_coord + ((self.size * self.r4) * math.cos(math.pi / 180 * angle ))
        y4 = self.y_coord + ((self.size * self.r4) * math.sin(math.pi / 180 * angle ))
        angle = angle + angle_inc
        x5 = self.x_coord + ((self.size * self.r5) * math.cos(math.pi / 180 * angle ))
        y5 = self.y_coord + ((self.size * self.r5) * math.sin(math.pi / 180 * angle ))
        angle = angle + angle_inc
        x6 = self.x_coord + ((self.size * self.r6) * math.cos(math.pi / 180 * angle ))
        y6 = self.y_coord + ((self.size * self.r6) * math.sin(math.pi / 180 * angle ))
        angle = angle + angle_inc
        x7 = self.x_coord + ((self.size * self.r7) * math.cos(math.pi / 180 * angle ))
        y7 = self.y_coord + ((self.size * self.r7) * math.sin(math.pi / 180 * angle ))
        angle = angle + angle_inc
        x8 = self.x_coord + ((self.size * self.r8) * math.cos(math.pi / 180 * angle ))
        y8 = self.y_coord + ((self.size * self.r8) * math.sin(math.pi / 180 * angle ))
        
        
               
        pygame.draw.polygon(SCREEN, self.color, [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8) ], self.width)
    

        #debugging points and sizes
        #SIZE_FONT = pygame.font.SysFont('arial', 20)

        #size_text = SIZE_FONT.render( str(self.size), 1, WHITE)
        #SCREEN.blit(size_text, ((self.x_coord - size_text.get_width()/2), (self.y_coord)))
    
        #SIZE_FONT = pygame.font.SysFont('arial', 20)

        #size_text = SIZE_FONT.render( str(self.points), 1, WHITE)
        #SCREEN.blit(size_text, ((self.x_coord - size_text.get_width()/2 ), (self.y_coord + 25)))
    

    #Method check_distance in Class Asteroid - check asteroid distance against bullet list    
    def check_distance(self, bullet_list):       
        i = 0
        while i < len(bullet_list):   
            d = math.sqrt(((bullet_list[i].x_coord - self.x_coord) ** 2) + ((bullet_list[i].y_coord - self.y_coord) ** 2) )
            if d <= bullet_list[i].size + self.size:
                self.hit = 1
                #self.speed = 0
                return(1)
            i = i + 1
        return(0)

    #not being used
    def check_distance_spaceship(self, spaceship):       

        d = math.sqrt(((spaceship.x_coord - self.x_coord) ** 2) + ((spaceship.y_coord - self.y_coord) ** 2) )
        if d <= spaceship.size + self.size:
            self.hit = 1
            #self.speed = 0
            return(1)


        
        return(0)
        