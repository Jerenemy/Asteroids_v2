import pygame
from sys import exit
import math
import random
import os
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

bip1 = pygame.mixer.Sound(os.path.join('Asteroids II', 'Assets', 'AsteroidSounds', 'beat1.wav'))
bip2 = pygame.mixer.Sound(os.path.join('Asteroids II', 'Assets', 'AsteroidSounds', 'beat2.wav'))

#*******************************************CLASSES*******************************************

class Level:
    def __init__(self):
        
        self.current_counter = 0
        self.level_counter = 0
        self.restart_counter = 0



        #BIP
        self.main_bip_counter = 0
        #self.phase_1_bip_delta_time = 100
        self.bip_delta_time_factor = 1
        self.bip_delta_time = 120
        

        self.bip_offset = 50
        self.next_bip1_sound = self.bip_offset
        self.next_bip2_sound = self.bip_offset
        self.restart_bip_level_counter = 0
        self.bip12_counter_reset = 0

        self.bip_pause_counter_reset = 0
        
        self.bip_init_phase_1 = 100
        self.bip_init_phase_2 = 200
        self.bip_init_phase_3 = 300

        self.bip_phase_1 = 100
        self.bip_phase_2 = 200
        self.bip_phase_3 = 300

        self.pause_counter_bip = 0

        self.bip_phases_completed = 1
        self.restart_bip_initiate = 0


        self.initial_bip_phases_completion_counter = self.bip_phase_3 + self.bip_phase_1
        self.bip_phases_completion_counter = self.initial_bip_phases_completion_counter
        self.bip_phases_completion_counter_reset = 0

    
    def bip_sound(self):
        
        #if self.main_bip_counter < self.phase_1:
        if self.main_bip_counter == self.next_bip1_sound:
            bip1.play()
            self.next_bip2_sound = self.main_bip_counter + self.bip_delta_time/2 
            self.next_bip1_sound = self.main_bip_counter + self.bip_delta_time
        if self.main_bip_counter == self.next_bip2_sound != self.next_bip1_sound:
            bip2.play()
            self.next_bip2_sound = self.main_bip_counter + self.next_bip2_sound + self.bip_delta_time

    def bip_phases_increase(self):
        self.bip_delta_time = 120 / self.bip_delta_time_factor

        if self.main_bip_counter / self.bip_phase_1 < 1:
            self.bip_delta_time_factor = 1
        elif self.main_bip_counter / self.bip_phase_2 < 1 < self.main_bip_counter / self.bip_phase_1:
            self.bip_delta_time_factor = 2
        else:
            self.bip_delta_time_factor = 2*2

    def bip_pause_fix(self):
        self.next_bip1_sound = self.next_bip2_sound = self.main_bip_counter + self.bip_offset

    def bip_pause_fix2(self):
        if self.next_bip1_sound < self.main_bip_counter:
            
            self.next_bip1_sound = self.next_bip1_sound + self.bip_delta_time
        
        if self.next_bip2_sound < self.main_bip_counter:
            
            self.next_bip2_sound = self.next_bip2_sound + self.bip_delta_time


            
