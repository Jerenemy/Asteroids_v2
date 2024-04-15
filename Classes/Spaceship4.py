import pygame
#from sys import exit
import math
#import random
pygame.display.init()
pygame.font.init()

import pygame
import math
import random
import os

from Classes.BulletList import BulletList


pygame.display.init()
pygame.font.init()
#pygame.mixer()

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
ORANGE = (255, 140, 0)


#SPACESHIP MOVEMENT
ACCELERATION = 0.25
DECELERATION = 0.1
ROTATE = 7

RAD2DEG = 180 / math.pi
DEG2RAD = math.pi / 180


"""bang_sship_auto_destroy = pygame.mixer.Sound(os.path.join('Asteroids', 'AsteroidSounds', 'bangSmall.wav'))
bang_sship_destroy = pygame.mixer.Sound(os.path.join('Asteroids', 'AsteroidSounds', 'bangMedium.wav'))

bang_sship_auto_destroy = pygame.mixer.Sound(os.path.join('AsteroidSounds', 'bangSmall.wav'))
bang_sship_destroy = pygame.mixer.Sound(os.path.join('AsteroidSounds', 'bangMedium.wav'))
"""

#Class Spaceship ******************************************
class Spaceship:
    def __init__(self, color, x_coord, y_coord, size, speed, direction, orientation):
        self.color = color
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.size = size
        self.speed = speed
        self.direction = direction
        self.orientation = orientation
        self.width = 3
        self.destroy_spaceship = 0
        self.destroy_counter = 0
        self.end_destroy_counter = 250
        
        self.lives = -2 #3
        
        self.rocket = 0
        self.rocket_counter = 0
        self.rocket_sound_counter = 0
        self.score = 0
        self.game_over_true = 0
        self.high_score = 0
        self.start_game = 0
        self.restart_tick_time = 0
        self.restart_counter_initiate = 0
        
        self.automated = 0

        self.spaceship_destroy_sound_play = 0

        self.invulnerability = 0
        self.invulnerability_counter = 0
        self.invulnerability_counter_end = 150
        self.invulnerability_counter_color = 0
        self.invulnerability_counter_color_delta = 20
        self.paused_true = 0

        self.rocket_color = WHITE

        #######
        
        

        self.refresh_screen = 0

        
        




        

        ###AUTOMATED
        self.display_spaceship_automated = 1
        self.hit = 0

    
        
    
    #Method move in Class Spaceship
    def move(self):
        
        self.x_coord = self.x_coord + (self.speed * math.cos(math.pi / 180 * (self.direction - 90) ))
        self.y_coord = self.y_coord + (self.speed * math.sin(math.pi / 180 * (self.direction - 90) ))
        
        keys_pressed = pygame.key.get_pressed()
                
        if (keys_pressed[pygame.K_UP]) and self.destroy_spaceship == 0: #or keys_pressed[pygame.K_w]
            
            self.rocket = 1

            a = ACCELERATION
            c = self.speed
            
            B = 180 - (self.orientation - self.direction)
            
            new_speed = math.sqrt( (a ** 2) + (c ** 2) - (2 * a * c * math.cos(B * DEG2RAD)))

            #account for division by zero error
            #maybe fixed by using law of sines with angle on bottom, maybe not though

            if new_speed != 0:
                new_direction_radians = math.asin((a * math.sin(B*DEG2RAD)) / new_speed)
                
                new_direction = new_direction_radians * RAD2DEG + self.direction

                if new_direction >= 360:
                    new_direction = new_direction - 360
                elif new_direction <= 0:
                    new_direction = new_direction + 360
                
                self.direction = new_direction

            if new_speed == 0: 
                self.speed = 0

            self.speed = new_speed
            
        if (keys_pressed[pygame.K_LEFT]) and self.destroy_spaceship == 0: #or keys_pressed[pygame.K_a]
            if self.orientation < ROTATE:
                self.orientation = self.orientation + 360 - ROTATE
            else:
                self.orientation = self.orientation - ROTATE
        if (keys_pressed[pygame.K_RIGHT]) and self.destroy_spaceship == 0: #or keys_pressed[pygame.K_d]
            if self.orientation > 360 - ROTATE:
                self.orientation = self.orientation - 360 + ROTATE
            else:
                self.orientation = self.orientation + ROTATE
        else:
            if self.destroy_spaceship == 0:
                if self.speed > DECELERATION:  
                    self.speed = self.speed - DECELERATION
                else:
                    self.speed = 0
            if self.destroy_spaceship == 1:
                if self.speed > 20*DECELERATION:  
                    self.speed = self.speed - DECELERATION
                #else:
                    #self.speed = 0
                                       

        #relocate spaceship when it goes off the SCREEN
        if self.destroy_spaceship == 0:
            if self.x_coord < 0: self.x_coord = self.x_coord + X_SCRNSIZE
            if self.x_coord > X_SCRNSIZE: self.x_coord = self.x_coord - X_SCRNSIZE
            if self.y_coord < 0: self.y_coord = self.y_coord + Y_SCRNSIZE
            if self.y_coord > Y_SCRNSIZE: self.y_coord = self.y_coord - Y_SCRNSIZE

    
    #fix bullet bug: if bullet == 0, bullet deleted
    #Method display in Class Spaceship
    def display(self):
        
        #define coordinate for front of spacecraft
        x_front = self.x_coord + (self.size * math.cos(math.pi / 180 * (self.orientation - 90) ))
        y_front = self.y_coord + (self.size * math.sin(math.pi / 180 * (self.orientation - 90) ))

        #define coordinate for back right of spacecraft
        x_backright = self.x_coord + ((self.size * .8) * math.cos(math.pi / 180 * (140 + 15 + self.orientation - 90) ))
        y_backright = self.y_coord + ((self.size * .8) * math.sin(math.pi / 180 * (140 + 15 + self.orientation - 90) ))
  
        #define coordinate for back left of spacecraft
        x_backleft = self.x_coord + ((self.size * .8) * math.cos(math.pi / 180 * (220 - 15 + self.orientation - 90) ))
        y_backleft = self.y_coord + ((self.size * .8) * math.sin(math.pi / 180 * (220 - 15 + self.orientation - 90) ))
        
        #define coordinate for back right of spacecraft
        x_endright = self.x_coord + ((self.size * 1.4) * math.cos(math.pi / 180 * (140 + 20 + self.orientation - 90) ))
        y_endright = self.y_coord + ((self.size * 1.4) * math.sin(math.pi / 180 * (140 + 20 + self.orientation - 90) ))
  
        #define coordinate for back left of spacecraft
        x_endleft = self.x_coord + ((self.size * 1.4) * math.cos(math.pi / 180 * (220 - 20 + self.orientation - 90) ))
        y_endleft = self.y_coord + ((self.size * 1.4) * math.sin(math.pi / 180 * (220 - 20 + self.orientation - 90) ))    
        
        pygame.draw.polygon(SCREEN, self.color, [(x_front, y_front), (x_endright, y_endright), (x_backright, y_backright), (x_backleft, y_backleft), (x_endleft, y_endleft)], self.width)


        #ROCKETS
        x_rocket = self.x_coord + ((self.size * 1.4) * math.cos(math.pi / 180 * (180 + self.orientation - 90) ))
        y_rocket = self.y_coord + ((self.size * 1.4) * math.sin(math.pi / 180 * (180 + self.orientation - 90) ))
        
        x_rocketleft = self.x_coord + ((self.size * .8) * math.cos(math.pi / 180 * (180 + 20 + self.orientation - 90) ))
        y_rocketleft = self.y_coord + ((self.size * .8) * math.sin(math.pi / 180 * (180 + 20 + self.orientation - 90) ))    
        
        x_rocketright = self.x_coord + ((self.size * .8) * math.cos(math.pi / 180 * (180 - 20 + self.orientation - 90) ))
        y_rocketright = self.y_coord + ((self.size * .8) * math.sin(math.pi / 180 * (180 - 20 + self.orientation - 90) ))
  
        #rocket_width = 2
        if self.invulnerability == 0:
            if self.rocket_counter <= 2:
                self.rocket_color = WHITE
            if self.rocket_counter > 2:
                self.rocket_color = BLACK
            
            self.rocket_counter += 1

            if self.rocket_counter >= 4:
                self.rocket_counter = 0


        if self.rocket == 1:
            pygame.draw.polygon(SCREEN, self.rocket_color, [(x_rocket, y_rocket), (x_rocketleft, y_rocketleft), (x_rocketright, y_rocketright)], self.width)
            self.rocket = 0


    def destroy(self):
        
        #INITIAL LINES

        #line 1
        #front left of spacecraft
        x_frontleft = self.x_coord + (self.size * math.cos(math.pi / 180 * ( self.orientation - 90) )) 
        y_frontleft = self.y_coord + (self.size * math.sin(math.pi / 180 * ( self.orientation - 90) )) 
        #end left of spacecraft
        x_endleft = self.x_coord + ((self.size * 1.4) * math.cos(math.pi / 180 * (200 + self.orientation - 90) )) 
        y_endleft = self.y_coord + ((self.size * 1.4) * math.sin(math.pi / 180 * (200 + self.orientation - 90) ))  
        
        #line 2
        #front right of spacecraft
        x_frontright = self.x_coord + (self.size * math.cos(math.pi / 180 * (self.orientation - 90) )) 
        y_frontright = self.y_coord + (self.size * math.sin(math.pi / 180 * (self.orientation - 90) )) 
        #end right of spacecraft
        x_endright = self.x_coord + ((self.size * 1.4) * math.cos(math.pi / 180 * (160 + self.orientation - 90) )) 
        y_endright = self.y_coord + ((self.size * 1.4) * math.sin(math.pi / 180 * (160 + self.orientation - 90) ))  

        #line 3
        #back left of spacecraft
        x_backleft = self.x_coord + ((self.size * .8) * math.cos(math.pi / 180 * (205 + self.orientation - 90) )) 
        y_backleft = self.y_coord + ((self.size * .8) * math.sin(math.pi / 180 * (205 + self.orientation - 90) )) 
        #back right of spacecraft
        x_backright = self.x_coord + ((self.size * .8) * math.cos(math.pi / 180 * (155 + self.orientation - 90) )) 
        y_backright = self.y_coord + ((self.size * .8) * math.sin(math.pi / 180 * (155 + self.orientation - 90) )) 
  
        
        #NEW LINES

        #speed of destruction of spaceship (higher #, slower speed traveled)
        #destroy_dis = 100
        #max distance of destruction of spaceship (lower #, further distance)
        #destroy_dis1 = 1.5

        destroy_angle1 = -90
        destroy_angle2 = 90
        destroy_angle3 = 180

        #speed and distance of destruction of spaceship formula
        #destroy_dis_sship = (self.destroy_counter / destroy_dis1) * (self.end_destroy_counter /  (self.destroy_counter + destroy_dis) )
        destroy_dis_sship = self.destroy_counter

        #new line 1 position
        x_frontleft = x_frontleft + ( destroy_dis_sship )  * math.cos(math.pi / 180 * (self.orientation - 90 + destroy_angle1) )
        y_frontleft = y_frontleft + ( destroy_dis_sship )  * math.sin(math.pi / 180 * (self.orientation - 90 + destroy_angle1) )
        
        x_endleft = x_endleft + ( destroy_dis_sship )  * math.cos(math.pi / 180 * (self.orientation - 90 + destroy_angle1) )
        y_endleft = y_endleft + ( destroy_dis_sship )  * math.sin(math.pi / 180 * (self.orientation - 90 + destroy_angle1) )
        
        #new line 2 position
        x_frontright = x_frontright + ( destroy_dis_sship )  * math.cos(math.pi / 180 * (self.orientation - 90 + destroy_angle2) )
        y_frontright = y_frontright + ( destroy_dis_sship )  * math.sin(math.pi / 180 * (self.orientation - 90 + destroy_angle2) )
        
        x_endright = x_endright + ( destroy_dis_sship )  * math.cos(math.pi / 180 * (self.orientation - 90 + destroy_angle2) )
        y_endright = y_endright + ( destroy_dis_sship )  * math.sin(math.pi / 180 * (self.orientation - 90 + destroy_angle2) )
        
        #new line 3 position
        x_backleft = x_backleft + ( destroy_dis_sship )  * math.cos(math.pi / 180 * (self.orientation - 90 + destroy_angle3) )
        y_backleft = y_backleft + ( destroy_dis_sship )  * math.sin(math.pi / 180 * (self.orientation - 90 + destroy_angle3) )
        
        x_backright = x_backright + ( destroy_dis_sship )  * math.cos(math.pi / 180 * (self.orientation - 90 + destroy_angle3) )
        y_backright = y_backright + ( destroy_dis_sship )  * math.sin(math.pi / 180 * (self.orientation - 90 + destroy_angle3) )
        
        destroy_counter_ratio = self.destroy_counter/self.end_destroy_counter
        end_color_destroy_counter = self.end_destroy_counter/2
        destroy_counter_color_ratio = self.destroy_counter/end_color_destroy_counter
        
        if destroy_counter_color_ratio <= 1:
            destroy_color = ( (255 - destroy_counter_color_ratio * 255), (255 - destroy_counter_color_ratio * 255), (255 - destroy_counter_color_ratio * 255))
        else: 
            destroy_color = ( 0, 0, 0 )

        #line1 = pygame.draw.line(SCREEN, destroy_color, [x_frontleft, y_frontleft], [x_endleft, y_endleft], self.width)
        #line2 = pygame.draw.line(SCREEN, destroy_color, [x_frontright, y_frontright], [x_endright, y_endright], self.width)
        #line3 = pygame.draw.line(SCREEN, destroy_color, [x_backleft, y_backleft], [x_backright, y_backright], self.width)

        line1 = Line(x_frontleft, y_frontleft, x_endleft, y_endleft, destroy_color)
        line2 = Line(x_frontright, y_frontright, x_endright, y_endright, destroy_color)
        line3 = Line(x_backleft, y_backleft, x_backright, y_backright, destroy_color)
        

        angle = self.destroy_counter
        
        #dt = 10
        #clock = pygame.time.Clock()"""
        #angle = 0.5 * dt
        
        line1.rotate(2.5*angle)
        line1.draw(SCREEN)
        line2.rotate(-2.5*angle)
        line2.draw(SCREEN)
        line3.rotate(6*angle)
        line3.draw(SCREEN)

        #dt = clock.tick(60) + 10
        if self.paused_true == 0:
            self.destroy_counter += 1
        if self.destroy_counter == 1 and self.paused_true == 0:
            self.spaceship_destroy_sound_play = 1

        

        #self.speed = 0

        if self.destroy_counter >= self.end_destroy_counter:
            self.x_coord = X_SCRNSIZE/2
            self.y_coord = Y_SCRNSIZE/2
            self.direction = 0
            self.orientation = 0
            self.speed = 0
            destroy_color = WHITE
            self.destroy_counter = 0
            self.lives = self.lives - 1
            self.destroy_spaceship = 0
            self.rocket = 0
            self.hit = 0
            self.invulnerability = 1
            self.color = WHITE

    def invulnerable(self):
        if self.invulnerability == 1 and self.paused_true == 0:
            self.invulnerability_counter += 1
            if self.invulnerability_counter_color < self.invulnerability_counter_color_delta:
                self.color = WHITE
                #rocket color fix: black when sship is black
                if self.rocket_counter <= 2:
                    self.rocket_color = WHITE
                if self.rocket_counter > 2:
                    self.rocket_color = BLACK
                
                self.rocket_counter += 1

                if self.rocket_counter >= 4:
                    self.rocket_counter = 0
            
            if self.invulnerability_counter_color >= self.invulnerability_counter_color_delta:
                self.color = BLACK
                self.rocket_color = BLACK
            
            self.invulnerability_counter_color += 1

            if self.invulnerability_counter_color >= self.invulnerability_counter_color_delta * 1.5:
                self.invulnerability_counter_color = 0
            if self.invulnerability_counter > self.invulnerability_counter_end - 1:
                self.color = WHITE

        if self.invulnerability_counter >= self.invulnerability_counter_end:
            self.invulnerability = 0
            self.invulnerability_counter = 0
            self.invulnerability_counter_color = 0
    #Method check_distance in Class Spaceship - check asteroids distance against spaceship    
    def check_distance(self, space_object_list):       
        i = 0
        while i < len(space_object_list):   
            d = math.sqrt(((space_object_list[i].x_coord - self.x_coord) ** 2) + ((space_object_list[i].y_coord - self.y_coord) ** 2) )
            if d < space_object_list[i].size + self.size:
                return(1)            
            i = i + 1
        return(0)

    
    

    def score_display(self):

        SCORE_FONT = pygame.font.SysFont('keyboard', 50)

        score_text = SCORE_FONT.render( str(self.score), 1, WHITE)
        SCREEN.blit(score_text, ((X_SCRNSIZE - score_text.get_width() - 40), (score_text.get_height() - 30)))


    def game_over(self):
        WINNER_FONT = pygame.font.SysFont('keyboard', 100)
        WINNER_TEXT = "GAME OVER"
        
        draw_text = WINNER_FONT.render(WINNER_TEXT, 1, WHITE)
        SCREEN.blit(draw_text, (X_SCRNSIZE/2 - draw_text.get_width() / 2, Y_SCRNSIZE/2 - draw_text.get_height() / 2 - 10))
        
        

    def restart(self, event):
        RESTART_FONT = pygame.font.SysFont('keyboard', 30)
        RESTART_TEXT = "CLICK TO PLAY"
        draw_text1 = RESTART_FONT.render(RESTART_TEXT, 1, WHITE)
        SCREEN.blit(draw_text1, (X_SCRNSIZE/2 - draw_text1.get_width() / 2, Y_SCRNSIZE/2 - draw_text1.get_height()/2 + 65))
        
        keys_pressed = pygame.key.get_pressed()        

        if event.type == pygame.MOUSEBUTTONDOWN or keys_pressed[pygame.K_SPACE]:
            self.lives = 3
            self.score = 0
            self.refresh_screen = 1
            self.game_over_true = 0
            self.restart_tick_time = pygame.time.get_ticks()
            self.restart_counter_initiate = 1
            self.invulnerability = 0
            self.invulnerability_counter = 0
            self.color = WHITE


            
    def restart_lives1(self, event):
        RESTART_FONT = pygame.font.SysFont('keyboard', 30)
        RESTART_TEXT = "CLICK TO PLAY"
        draw_text1 = RESTART_FONT.render(RESTART_TEXT, 1, WHITE)
        SCREEN.blit(draw_text1, (X_SCRNSIZE/2 - draw_text1.get_width() / 2, Y_SCRNSIZE/2 - draw_text1.get_height()/2 + 65))
        
        keys_pressed = pygame.key.get_pressed()        

        if event.type == pygame.MOUSEBUTTONDOWN or keys_pressed[pygame.K_SPACE]:
            self.lives = 1
            self.score = 0
            self.refresh_screen = 1
            self.game_over_true = 0
            self.restart_tick_time = pygame.time.get_ticks()
            self.restart_counter_initiate = 1
            self.invulnerability = 0
            self.invulnerability_counter = 0
            self.color = WHITE


    def display_high_score(self):
        
        if self.high_score < self.score:
            self.high_score = self.score
        HIGH_SCORE_FONT = pygame.font.SysFont('keyboard', 20)
        HIGH_SCORE_FONT1 = pygame.font.SysFont('keyboard', 30)

        HIGH_SCORE_TEXT1 = "HIGH SCORE" 
        HIGH_SCORE_TEXT2 = str(self.high_score)
        h1 = HIGH_SCORE_FONT.render(HIGH_SCORE_TEXT1, 1, WHITE)
        h2 = HIGH_SCORE_FONT1.render(HIGH_SCORE_TEXT2, 1, WHITE)
        SCREEN.blit(h1, ( X_SCRNSIZE/2 - h1.get_width()/2 , 40 + 0 ))
        SCREEN.blit(h2, ( X_SCRNSIZE/2 - h2.get_width()/2 , 40 + h1.get_height()))
    
    def start(self, event):

        RESTART_FONT = pygame.font.SysFont('keyboard', 30)
        RESTART_TEXT = "CLICK TO PLAY"
        draw_text1 = RESTART_FONT.render(RESTART_TEXT, 1, WHITE)
        SCREEN.blit(draw_text1, (X_SCRNSIZE/2 - draw_text1.get_width() / 2, Y_SCRNSIZE/2 - draw_text1.get_height()/2 + 65))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.lives = 3
            self.start_game = 1

    def check_distance_bullets(self, bullet_list):       
            i = 0
            while i < len(bullet_list):   
                d = math.sqrt(((bullet_list[i].x_coord - self.x_coord) ** 2) + ((bullet_list[i].y_coord - self.y_coord) ** 2) )
                if d <= bullet_list[i].size + self.size:
                    self.hit = 1
                    #self.speed = 0
                    return(1)
                i = i + 1
            return(0)

    def reset_counters(self):
        self.invulnerability = 0
        self.invulnerability_counter = 0
        self.invulnerability_counter_color = 0
        self.destroy_spaceship = 0
        self.destroy_counter = 0
        




class SpaceshipLives(Spaceship):
    
    pass
    def __init__(self, color, x_coord, y_coord, size, speed, direction, orientation):
        super().__init__(color, x_coord, y_coord, size, speed, direction, orientation)
        self.sship3_x_coord = 140
        self.sship321_y_coord = 60
        self.sship2_x_coord = 100
        self.sship1_x_coord = 60

        self.start_get_new_spaceship_x = 6/8
        self.end_get_new_spaceship_x = 7/8
        self.start_get_new_spaceship_y = 15/16
        self.end_get_new_spaceship_y = 1

        self.new_spaceship_distance3 = X_SCRNSIZE/2 - 140
        self.new_spaceship_distance2 = X_SCRNSIZE/2 - 100
        self.new_spaceship_distance1 = X_SCRNSIZE/2 - 60
        self.new_spaceship_counter = 0
        self.end_new_spaceship_counter = self.end_destroy_counter


    def get_new_spaceship3(self):
        
        #TIME THIS PROPERLY USING RATIOS
        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_x and self.new_spaceship_counter < self.end_new_spaceship_counter * self.end_get_new_spaceship_x:
            if self.x_coord <= X_SCRNSIZE/2 - (X_SCRNSIZE/2 - self.sship3_x_coord) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x)):
                self.x_coord += (X_SCRNSIZE/2 - self.sship3_x_coord) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x))
            else:
                self.x_coord = X_SCRNSIZE/2

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_y:   
            self.x_coord == X_SCRNSIZE/2
            self.y_coord += (Y_SCRNSIZE/2 - self.sship321_y_coord) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_y - self.start_get_new_spaceship_y))
                
        self.new_spaceship_counter += 1
            #self.destroy_counter
            #self.end_destroy_counter
        

    def get_new_spaceship2(self):
        

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_x and self.new_spaceship_counter < self.end_new_spaceship_counter * self.end_get_new_spaceship_x:
            if self.x_coord <= X_SCRNSIZE/2 - (X_SCRNSIZE/2 - self.sship2_x_coord) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x)):
                self.x_coord += (X_SCRNSIZE/2 - self.sship2_x_coord) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x))
            else:
                self.x_coord = X_SCRNSIZE/2

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_y:   
            self.x_coord == X_SCRNSIZE/2
            self.y_coord += (Y_SCRNSIZE/2 - self.sship321_y_coord) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_y - self.start_get_new_spaceship_y))
                
        self.new_spaceship_counter += 1

    
    def get_new_spaceship1(self):
        

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_x and self.new_spaceship_counter < self.end_new_spaceship_counter * self.end_get_new_spaceship_x:
            if self.x_coord <= X_SCRNSIZE/2 - (X_SCRNSIZE/2 - self.sship1_x_coord) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x)):
                self.x_coord += (X_SCRNSIZE/2 - self.sship1_x_coord) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x))
            else:
                self.x_coord = X_SCRNSIZE/2

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_y:   
            self.x_coord == X_SCRNSIZE/2
            self.y_coord += (Y_SCRNSIZE/2 - self.sship321_y_coord) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_y - self.start_get_new_spaceship_y))
                
        if self.paused_true == 0:
            self.new_spaceship_counter += 1

    def revert_spaceship3(self):
        self.x_coord = self.sship3_x_coord
        self.y_coord = self.sship321_y_coord
        self.new_spaceship_counter = 0

    def revert_spaceship2(self):
        self.x_coord = self.sship2_x_coord
        self.y_coord = self.sship321_y_coord
        self.new_spaceship_counter = 0

    def revert_spaceship1(self):
        self.x_coord = self.sship1_x_coord
        self.y_coord = self.sship321_y_coord
        self.new_spaceship_counter = 0


class Line: 
    def __init__(self, x0, y0, x1, y1, color):
        self.color = color
        self.width = 3
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.center_x = (x1 + x0) / 2
        self.center_y = (y1 + y0) / 2

        self.half_length = math.hypot(x1 - x0, y1 - y0) / 2
        self.angle = math.atan2(0 - y1, x1 - x0)

    def rotate(self, angle):
        #rotates line by given angle in degrees
        angle *= math.pi / 180
        self.angle += angle
        dx = self.half_length * math.cos(self.angle)
        dy = -self.half_length * math.sin(self.angle)
        self.x0 = self.center_x - dx
        self.y0 = self.center_y - dy
        self.x1 = self.center_x + dx
        self.y1 = self.center_y + dy

    def draw(self, surface):
        pygame.draw.line(surface,
                         self.color,
                         (self.x0, self.y0),
                         (self.x1, self.y1),
                         self.width)

bullet_collection = BulletList()

# CLASS SpaceshipAutomated ******************************************************************************************************    
class SpaceshipAutomated(Spaceship):
    def __init__(self, color, x_coord, y_coord, size, speed, direction, orientation):
        super().__init__(color, x_coord, y_coord, size, speed, direction, orientation)

        
        
        #self.color_change = bullet_collection.bullet_accuracy / (24/17)
        self.color_change = 0
        self.color = (255, self.color_change, self.color_change)
        self.width = 3
        self.destroy_spaceship = 0
        
        
        
        
        self.score = 0
        self.game_over_true = 0
        self.high_score = 0
        self.start_game = 0
        self.restart_tick_time = 0

        self.automated = 1
        
        self.points = 500


        #super().__init__()"""

    
    def display(self):
        
        #LEFT
        #1,2,3,4
        xL1 = self.x_coord + (self.size * .9 * math.cos(math.pi / 180 * (350 + self.orientation - 90) ))
        yL1 = self.y_coord + (self.size * .9 * math.sin(math.pi / 180 * (350 + self.orientation - 90) ))


        xL2 = self.x_coord + (self.size * .6 * math.cos(math.pi / 180 * (360 - 45 + self.orientation - 90) ))
        yL2 = self.y_coord + (self.size * .6 * math.sin(math.pi / 180 * (360 - 45 + self.orientation - 90) ))

        xL3 = self.x_coord + (self.size * 1 * math.cos(math.pi / 180 * (270 + self.orientation - 90) ))
        yL3 = self.y_coord + (self.size * 1 * math.sin(math.pi / 180 * (270 + self.orientation - 90) ))

        xL4 = self.x_coord + (self.size * .8 * math.cos(math.pi / 180 * (225 + self.orientation - 90) ))
        yL4 = self.y_coord + (self.size * .8 * math.sin(math.pi / 180 * (225 + self.orientation - 90) ))

        #RIGHT
        xR1 = self.x_coord + (self.size * .9 * math.cos(math.pi / 180 * (10 + self.orientation - 90) ))
        yR1 = self.y_coord + (self.size * .9 * math.sin(math.pi / 180 * (10 + self.orientation - 90) ))


        xR2 = self.x_coord + (self.size * .6 * math.cos(math.pi / 180 * (45 + self.orientation - 90) ))
        yR2 = self.y_coord + (self.size * .6 * math.sin(math.pi / 180 * (45 + self.orientation - 90) ))

        xR3 = self.x_coord + (self.size * 1 * math.cos(math.pi / 180 * (90 + self.orientation - 90) ))
        yR3 = self.y_coord + (self.size * 1 * math.sin(math.pi / 180 * (90 + self.orientation - 90) ))

        xR4 = self.x_coord + (self.size * .8 * math.cos(math.pi / 180 * (135 + self.orientation - 90) ))
        yR4 = self.y_coord + (self.size * .8 * math.sin(math.pi / 180 * (135 + self.orientation - 90) ))

        pygame.draw.polygon(SCREEN, self.color, [(xL1,yL1), (xL2,yL2), (xR2,yR2), (xL2,yL2), (xL3,yL3), (xR3,yR3), (xL3,yL3), (xL4,yL4), (xR4,yR4), (xR3,yR3), (xR2,yR2), (xR1,yR1)], self.width)




    def move(self):
        self.x_coord = self.x_coord + (self.speed * math.cos(math.pi / 180 * (self.direction - 90) ))
        self.y_coord = self.y_coord + (self.speed * math.sin(math.pi / 180 * (self.direction - 90) ))    

    def generate_random(self):
        random_num = random.randrange(1, 3, 1)
        #random_size = random.randrange(10,50,20)
        
        #self.speed = 10
        #random_size = random.randrange(30, 50, 5)

        
        
        if random_num == 1: 
            self.color = (255, round(self.color_change), round(self.color_change))
            self.x_coord = X_SCRNSIZE + 40
            self.y_coord = random.randrange(1, Y_SCRNSIZE, 1)
            #self.size = random_size
            #self.direction = random.randrange(180, 360,1)
            self.direction = 270
 
        
        if random_num == 2: 
            self.color = (255, round(self.color_change), round(self.color_change))
            self.x_coord = -40
            self.y_coord = random.randrange(1, Y_SCRNSIZE, 1)
            #self.size = random_size
            #self.direction = random.randrange(0, 180,1)
            self.direction = 90
            

class SpaceshipAutomatedList( list ):
    def __init__(self):
        self.spaceship_auto_destroy_sound_play = 0
        self.change_direction_amount = 0
        self.random_direction_amount = 0

    #Method change spaceships direction in Class SpaceshipAutomatedList:
    def change_directions(self, manned_sship):       
        i = 0
        
        while i < len(self):   
            """if self.change_direction_amount != 0:
                self.random_direction_amount = random.randrange(round(-self.change_direction_amount),round(self.change_direction_amount),1)
            else:
                self.random_direction_amount = 0
            """

            xx = manned_sship.x_coord - self[i].x_coord
            yy = manned_sship.y_coord - self[i].y_coord

            if xx < 0:
                self.change_direction_amount = (math.atan(yy/xx) - 90 * DEG2RAD) * RAD2DEG
            if xx > 0:
                self.change_direction_amount = (math.atan(yy/xx) + 90 * DEG2RAD) * RAD2DEG
            if xx == 0:
                if yy >= 0: 
                    self.change_direction_amount = 180
                if yy < 0:
                    self.change_direction_amount = 0

            self.change_direction_amount = self.change_direction_amount + self.random_direction_amount
            #self[i].direction = self[i].direction - self.change_direction_amount
            self[i].direction = self.change_direction_amount

            i = i + 1

    #Method move_asteroids in Class SpaceshipAutomatedList:
    def move_spaceships(self):       
        i = 0
        while i < len(self):   
            self[i].move()
            if self[i].x_coord < (0 - self[i].size) or self[i].x_coord > (X_SCRNSIZE + self[i].size) or self[i].y_coord < (0 - self[i].size) or  self[i].y_coord > (Y_SCRNSIZE + self[i].size): 
                self.pop(i)            
            i = i + 1

    #Method check_spaceships in Class SpaceshipAutomatedList:
    def check_if_spaceships_hit(self, bullet_list):       
        i = 0
        while i < len(self):   
            hit = self[i].check_distance(bullet_list)
            self[i].hit = hit
            i = i + 1
            

    #Method display_spaceships in Class SpaceshipAutomatedList:
    def display_spaceships(self):        
        i = 0
        while i < len(self):   
            self[i].display()
            i = i + 1


    def delete_hit_spaceships(self):       
        i = 0
        while i < len(self):   
            if self[i].hit == 1:
                #bang_sship_auto_destroy.play()
                self.spaceship_auto_destroy_sound_play = 1
                self.pop(i)            
            i = i + 1


