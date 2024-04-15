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
    def __init__(self, bullet_accuracy):
        
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

        self.sship_respawn = 0
        """
        #increase delta times func
        
        self.asteroid_delta_time = 0
        self.min_asteroid_delta_time = 0 
        #self.factor_asteroid_delta_time = 0
        self.min_spaceship_delta_time = 0
        self.max_spaceship_fire_delta_time = 0
        self.factor_spaceship_delta_time = 0
        self.factor_spaceship_fire_delta_time = 0

        #DELTA TIMES:"""
        self.next_level_time = 0
        #initial DELTA TIMES
        self.initial_spaceship_fire_delta_time = 500 #increases
        self.initial_asteroid_delta_time = 1200    
        self.initial_spaceship_delta_time = 6000 
        #dynamic DELTA TIMES
        self.spaceship_fire_delta_time = self.initial_spaceship_fire_delta_time #increases
        self.asteroid_delta_time = self.initial_asteroid_delta_time    
        self.spaceship_delta_time = self.initial_spaceship_delta_time 
        #static DELTA TIMES
        self.bullet_delta_time = 150
        self.rocket_sound_delta_time = 285 #ticks of rocket sound
        self.pause_delta_time = 500

        #MINIMUM DELTA TIMES:
        self.min_asteroid_delta_time = 450
        self.min_spaceship_delta_time = 2500
        self.max_spaceship_fire_delta_time = 1500

        #LEVEL FACTORS
        self.level_factor = .5

        self.factor_asteroid_delta_time = self.level_factor * 1.125
        self.factor_spaceship_delta_time = self.level_factor
        #factor_spaceship_fire_delta_time =  level_factor * 1.3125 #increasing 1.05
        self.factor_spaceship_fire_delta_time = 1.5
        self.factor_bullet_accuracy = self.level_factor * .9
        self.factor_color_change = .5 #not used

        ##### PASS bullet_collection.bullet_accuracy upon creating object (and when calling func)
        self.bullet_accuracy = bullet_accuracy
        self.factor_bullet_accuracy = self.level_factor * .9

        #difficulty level (should change all difficulty levels to something different than bip)
        self.level_delta_time = 1000
        



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

    def bip_counters_phases_increase(self):
        if self.level_counter == self.bip_phases_completion_counter:
            self.bip_phases_completed += 1
            #self.restart_bip_initiate = 1
            self.bip_phase_1 = (self.bip_phases_completed-1) * self.initial_bip_phases_completion_counter + self.bip_init_phase_1 
            self.bip_phase_2 = (self.bip_phases_completed-1) * self.initial_bip_phases_completion_counter + self.bip_init_phase_2 
            self.bip_phase_3 = (self.bip_phases_completed-1) * self.initial_bip_phases_completion_counter + self.bip_init_phase_3 
            #self.bip_delta_time_factor = 1
            self.bip_phases_completion_counter = self.bip_phases_completed*(self.initial_bip_phases_completion_counter) + self.bip_phases_completion_counter_reset      

    def bip_restart_counters(self):
        if self.restart_bip_initiate == 1:
            self.restart_bip_level_counter = 0
            self.next_bip1_sound = self.bip_offset
            self.next_bip2_sound = self.bip_offset
            self.bip_phases_completed = 1
            
            self.restart_bip_initiate = 0

    def bip12_counter_reset_func(self):
        if self.bip12_counter_reset == 1:
                self.restart_bip_level_counter = self.main_bip_counter 
                self.next_bip2_sound = self.next_bip1_sound = self.bip_offset

    def sship_respawn_func(self):
        if self.sship_respawn == 1:
            self.bip12_counter_reset += 1 
            self.bip_phases_completed = 1
            self.bip_phases_completion_counter_reset = self.bip_phases_completion_counter
            self.bip_phase_1 = self.bip_init_phase_1
            self.bip_phase_2 = self.bip_init_phase_2
            self.bip_phase_3 = self.bip_init_phase_3
        else:
            self.bip12_counter_reset = 0
    
    def increase_delta_times(self, bullet_accuracy):
        if self.level_counter == self.next_level_time:

            #increase/decrease DELTA TIMES as levels increase:
            if self.asteroid_delta_time > self.min_asteroid_delta_time:
                self.asteroid_delta_time = self.asteroid_delta_time * self.factor_asteroid_delta_time
            
            if self.spaceship_delta_time > self.min_spaceship_delta_time:
                self.spaceship_delta_time = self.spaceship_delta_time * self.factor_spaceship_delta_time
            
            if self.spaceship_fire_delta_time < self.max_spaceship_fire_delta_time:
                self.spaceship_fire_delta_time = self.spaceship_fire_delta_time * self.factor_spaceship_fire_delta_time
            #doesn't work yet, stays at 180
            if self.bullet_accuracy >= 0:
                bullet_accuracy = bullet_accuracy * self.factor_bullet_accuracy
            
            #sship_auto.color_change = sship_auto.color_change * factor_color_change/5 #PROBLEM: every time a new sship_auto is created, the color_change is reset to the init value

            self.next_level_time = self.level_counter + self.level_delta_time
