import pygame
from sys import exit
import math
import random

from Classes.Bullet import Bullet

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

#BULLET MOVEMENT
auto_bullet_speed = 5

#******************************************************* CLASSES *******************************************************

#Class BulletList - move bullets in list *************************************************
class BulletList(list):
    
    def __init__(self):
        self.bullet_accuracy = 360
        self.random_accuracy = 360
        

        super().__init__()
        
    #Method move_bullets in Class BulletList - move bullets in list
    def move_bullets(self):       
        i = 0
        while i < len(self):   
            self[i].move()
            if self[i].x_coord < (0 - self[i].size) or self[i].x_coord > (X_SCRNSIZE + self[i].size) or self[i].y_coord < (0 - self[i].size) or  self[i].y_coord > (Y_SCRNSIZE + self[i].size) or self[i].speed == 0: 
                self.pop(i)            
            i = i + 1

    #Method check_bullets in Class BulletList - check bullets in list against space object list
    def check_if_bullets_hit(self, space_object_list):       
        i = 0
        bullets_score = 0

        while i < len(self):   
            hit_points = self[i].check_distance(space_object_list)
            if hit_points > 0:
                self[i].hit = 1
            
                if self[i].bullet_source == 1:  
                    self[i].hit_points = hit_points
                    bullets_score = bullets_score + hit_points
            
            if self[i].x_coord < (0 - self[i].size) or self[i].x_coord > (X_SCRNSIZE + self[i].size) or self[i].y_coord < (0 - self[i].size) or  self[i].y_coord > (Y_SCRNSIZE + self[i].size): 
                self.pop(i)            
            i = i + 1

        return(bullets_score)

    
    #Method display_bullets in Class BulletList - display bullets in list:
    def display_bullets(self):        
        i = 0
        while i < len(self):   
            self[i].display()
            i = i + 1

    #Method delete_hit_bullets in Class BulletList - move bullets in list
    def delete_hit_bullets(self):       
        i = 0
        while i < len(self):   
            if self[i].hit == 1:
                self.pop(i)            
            i = i + 1

    #fire_automated_bullets in Class BulletList
    def fire_automated_bullets(self, space_ship_list, sship ):        
        i = 0

        while i < len(space_ship_list):   

            #generate random times that spaceships fire
            fire_trigger = random.randrange(1, 10, 1)

            if space_ship_list[i].automated == 1 and fire_trigger >= 8:
                #fire_direction = random.randrange(1,360,1)

                #FIXED FORMULA!!!
                #what to do when sship.x_coord = space_ship_list[i].x_coord

                #round(self.bullet_accuracy)
                if round(self.bullet_accuracy) != 0:
                    self.random_accuracy = random.randrange(round(-self.bullet_accuracy),round(self.bullet_accuracy),1)
                else:
                    self.random_accuracy = 0
                

                xx = sship.x_coord - space_ship_list[i].x_coord
                yy = sship.y_coord - space_ship_list[i].y_coord

                if xx < 0:
                    fire_direction = (math.atan(yy/xx) - 90 * DEG2RAD) * RAD2DEG
                if xx > 0:
                    fire_direction = (math.atan(yy/xx) + 90 * DEG2RAD) * RAD2DEG
                if xx == 0:
                    if yy >= 0: 
                        fire_direction = 180
                    if yy < 0:
                        fire_direction = 0

                fire_direction = fire_direction + self.random_accuracy


                #old formula(inaccurate)
                """yy = ((sship.y_coord - 90) * DEG2RAD) - (space_ship_list[i].y_coord * DEG2RAD)
                xx = ((sship.x_coord - 90) * DEG2RAD) - (space_ship_list[i].x_coord * DEG2RAD)
                
                fire_direction = (math.atan2(yy, xx) * RAD2DEG) + 90
                #define accuracy
                #fire_direction = fire_direction + random.randrange(-1, 1, 1)
                fire_direction = fire_direction"""

                bullet = Bullet(space_ship_list[i], auto_bullet_speed, fire_direction, 0 )
                self.append( bullet )
            i = i + 1

    #toggle bullet accuracy to be 0 or 360
    def toggle_bullet_accuracy(self, event):
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_0:
                    self.bullet_accuracy = 0
                if event.key == pygame.K_9:
                    self.bullet_accuracy = 360

    #display bullet accuracy on screen
    def display_bullet_accuracy(self):
        SIZE_FONT = pygame.font.SysFont('arial', 20)

        size_text = SIZE_FONT.render( str(self.bullet_accuracy), 1, WHITE)
        SCREEN.blit(size_text, ( 20 ,  Y_SCRNSIZE/2 ))
    



    