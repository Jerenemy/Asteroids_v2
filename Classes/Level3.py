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
#TO DO:
"""
add factors to phase_2 and phase_3 (phase_completed stupid variable name)
"""
class Level:
    def __init__(self):
        
        #MAIN COUNTERS
        self.main_counter = 0 #main counter that all other counters based off of
        self.level_counter = 0 # = main_counter - restart_counter; used to determine game level; reset to zero upon game restart
        self.restart_counter = 0 #subtracted counter: when restart initated, restart_counter = main_counter
        self.pause_counter_adjust = 0 #increases while game paused, subtracted from level_counter
        
        #BIP
        self.bip_delta_time_factor = 1 #goes from 1 to 2 to 4 as phases increase
        self.bip_delta_time = 120 #divided by bip_delta_time_factor
        self.offset = 20 #accounts for main_bip_counter not starting at 0, not allowing bip_sound method to take effect
        #next BIP times
        self.next_bip1_sound = self.offset
        self.next_bip2_sound = self.offset
        self.bip12_counter_reset = 0

        #initial bip phases times
        self.bip_init_phase_1 = 300
        self.bip_init_phase_2 = 600
        self.bip_init_phase_3 = 900

        #dynamic bip phases times
        self.bip_phase_1 = self.bip_init_phase_1
        self.bip_phase_2 = self.bip_init_phase_2
        self.bip_phase_3 = self.bip_init_phase_3

        
        self.bip_phase_length_increase_factor = 100 #FACTOR that determines how much waves get longer

        
        self.waves_completed = 1 #wave number player is one (waves completed is that - 1)
        self.max_waves_completed = 1 #high score of waves completed
        self.restart_bip_initiate = 0 #

        
        
        #difficulty level (should change all difficulty levels to something different than bip)
        self.level_delta_time = 100
        self.difficulty_level = 0
        self.initial_next_level_time = self.level_delta_time
        self.next_level_time = self.initial_next_level_time
        #initial DELTA TIMES
        self.initial_spaceship_fire_delta_time = 100 #increases
        self.initial_asteroid_delta_time = 200 #decreases 
        self.initial_spaceship_delta_time = 600 #decreases
        self.init_bullet_accuracy = 180
        #dynamic DELTA TIMES
        self.spaceship_fire_delta_time = self.initial_spaceship_fire_delta_time #increases
        self.asteroid_delta_time = self.initial_asteroid_delta_time    
        self.spaceship_delta_time = self.initial_spaceship_delta_time 
        #static DELTA TIMES - NOT YET IN USE
        self.bullet_delta_time = 150
        self.rocket_sound_delta_time = 285 #ticks of rocket sound
        #MINIMUM DELTA TIMES:
        self.min_asteroid_delta_time = 40
        self.min_spaceship_delta_time = 100
        self.max_spaceship_fire_delta_time = 1500
        #LEVEL FACTORS
        self.level_factor = .75
        self.factor_bullet_accuracy = self.level_factor
        self.factor_asteroid_delta_time = self.level_factor * 1.2
        self.factor_spaceship_delta_time = self.level_factor * 1.25
        self.factor_spaceship_fire_delta_time =  self.level_factor * 1.3125 #increasing 1.05
        self.factor_color_change = .5 #not used
        #NEXT TIMES
        self.next_asteroid_time = self.asteroid_delta_time
        self.next_spaceship_time = self.spaceship_delta_time
        self.next_spaceship_fire_time = self.spaceship_fire_delta_time
        #TRIGGERS
        self.init_next_difficulty_wave = 0 #trigger that next wave beginning
        self.sship_destroyed_counter_reset = 0

        #colors
        self.wave_color_counter = 0
        self.init_wave_display = 0
        self.init_wave_color_increase = 0
        self.init_wave_color_decrease = 0
        
        self.name_waves = ""
        self.name_points = ""
        self.current_name_waves = ""
        self.initial_1 = ""
        self.initial_2 = ""
        self.initials = ""
        
        self.fix = False
        self.fix_delta_time = 1
        self.fix_time = 0  
        self.switch = 0
        self.barrier_switch = 0
        self.last_i = 96
        self.last_i_2 = 96
        self.barrier_switch_2 = 0
        self.init_new_high_score = 0
        self.initial_start = 0
        
        self.hs_acc = ""
    def bip_sound(self, spaceship):
        """
        sig: Spaceship --> none
        plays bips (when sship not being destroyed) incrememted by bip_delta_time, increases next_bip counters
        must pass sship object
        """
        #if self.level_counter < self.phase_1:
        if self.level_counter == self.next_bip1_sound:
            if spaceship.destroy_spaceship == 0:
                bip1.play() 
            self.next_bip1_sound = self.level_counter + self.bip_delta_time
            self.next_bip2_sound = self.level_counter + self.bip_delta_time/2 
        elif self.level_counter == self.next_bip2_sound:
            if spaceship.destroy_spaceship == 0:
                bip2.play()
            #self.next_bip2_sound = self.level_counter + self.next_bip2_sound + self.bip_delta_time
        

    def bip_phases_increase(self):
        """
        sig: none --> none
        increases speed of bips in 3 phases by changing bip_delta_time by a factor of bip_delta_time_factor
        """
        self.bip_delta_time = 120 / self.bip_delta_time_factor

        if self.level_counter / self.bip_phase_1 < 1:
            self.bip_delta_time_factor = 1
        elif self.level_counter / self.bip_phase_2 < 1:
            self.bip_delta_time_factor = 2
        else:
            self.bip_delta_time_factor = 2*2

    
    def bip_counters_phases_increase(self):
        """
        sig: none --> none
        increases phases values 
        """
        if self.level_counter == self.bip_phase_3:
            self.waves_completed += 1
            #self.restart_bip_initiate = 1
            self.bip_phase_1 = self.bip_phase_3 + self.bip_init_phase_1 + self.bip_phase_length_increase_factor * self.waves_completed
            self.bip_phase_2 = self.bip_phase_3 + self.bip_init_phase_2 + self.bip_phase_length_increase_factor * self.waves_completed * 2
            self.bip_phase_3 = self.bip_phase_3 + self.bip_init_phase_3 + self.bip_phase_length_increase_factor * self.waves_completed * 3
            """self.bip_phase_1 = (self.waves_completed-1) * self.bip_init_phase_3 + self.bip_init_phase_1 + self.bip_phase_length_increase_factor * self.waves_completed
            self.bip_phase_2 = (self.waves_completed-1) * self.bip_init_phase_3 + self.bip_init_phase_2 + self.bip_phase_length_increase_factor * self.waves_completed
            self.bip_phase_3 = (self.waves_completed-1) * self.bip_init_phase_3 + self.bip_init_phase_3 + self.bip_phase_length_increase_factor * self.waves_completed
            """#self.bip_delta_time_factor = 1
            self.init_next_difficulty_wave = 1
      
    def next_difficulty_wave(self, bullet_accuracy):
        """
        sig: int/float --> int/float
        when triggered (all 3 phases completed, next wave begins), resets all enemy attributes to init, returns init_bullet_accuracy
        must pass bullet_collection.bullet_accuracy; must set bullet_collection.bullet_accuracy = function to call function
        """
        if self.init_next_difficulty_wave == 1:
            #self.restart_counter = self.main_counter - self.pause_counter_adjust
            
            #self.restart_bip_initiate = 1

            #time between levels
            #self.next_level_time = self.initial_next_level_time

            #reset DELTA TIMES
            self.spaceship_fire_delta_time = self.initial_spaceship_fire_delta_time
            self.asteroid_delta_time = self.initial_asteroid_delta_time    
            self.spaceship_delta_time = self.initial_spaceship_delta_time             
            bullet_accuracy = self.init_bullet_accuracy
            self.difficulty_level = 0
            self.init_wave_display = 1
            
            self.init_next_difficulty_wave = 0
        return bullet_accuracy
    def bip_restart_counters(self):
        """
        sig: none --> none
        when triggered (game starts/restarts), resets bip restart, next times, and phases completed counters 
        IN USE
        """
        if self.restart_bip_initiate == 1:
            self.next_bip1_sound = self.offset
            self.next_bip2_sound = self.offset
            self.bip_phase_1 = self.bip_init_phase_1
            self.bip_phase_2 = self.bip_init_phase_2
            self.bip_phase_3 = self.bip_init_phase_3
            self.waves_completed = 1 
            self.restart_bip_initiate = 0
            self.next_asteroid_time = self.asteroid_delta_time
            self.next_spaceship_time = self.spaceship_delta_time
            self.next_spaceship_fire_time = self.spaceship_fire_delta_time

    
    def increase_delta_times(self, bullet_accuracy):
        """
        sig: int/float --> none
        increases delta times of asteroids, auto sships and firing, and accuracy of auto sships based on level_counter
        must pass bullet_collection.bullet_accuracy
        """
        if self.level_counter == self.next_level_time:

            #increase/decrease DELTA TIMES as levels increase:
            if self.asteroid_delta_time > self.min_asteroid_delta_time:
                self.asteroid_delta_time = self.asteroid_delta_time * self.factor_asteroid_delta_time
            
            if self.spaceship_delta_time > self.min_spaceship_delta_time:
                self.spaceship_delta_time = self.spaceship_delta_time * self.factor_spaceship_delta_time
            
            if self.spaceship_fire_delta_time < self.max_spaceship_fire_delta_time:
                self.spaceship_fire_delta_time = self.spaceship_fire_delta_time * self.factor_spaceship_fire_delta_time
            #doesn't work yet, stays at 180
            if bullet_accuracy >= 0:
                bullet_accuracy = bullet_accuracy * self.factor_bullet_accuracy
            
            #sship_auto.color_change = sship_auto.color_change * factor_color_change/5 #PROBLEM: every time a new sship_auto is created, the color_change is reset to the init value

            self.next_level_time = self.level_counter + self.level_delta_time
            self.difficulty_level += 1
        return bullet_accuracy

    def reset_counters(self, spaceship):
        """
        sig: Spaceship --> none
        when triggered (new game started), sets level_counter = 0 (by changing restart_counter value) and resets next_level time and spaceship/asteroid delta times
        must pass sship object 
        """
        if spaceship.restart_counter_initiate == 1:
            self.restart_counter = self.main_counter - self.pause_counter_adjust
            
            self.restart_bip_initiate = 1

            #time between levels
            self.next_level_time = self.initial_next_level_time

            #reset DELTA TIMES
            self.spaceship_fire_delta_time = self.initial_spaceship_fire_delta_time
            self.asteroid_delta_time = self.initial_asteroid_delta_time    
            self.spaceship_delta_time = self.initial_spaceship_delta_time             
            self.difficulty_level = 0
            spaceship.restart_counter_initiate = 0
        
        #no need to return bullet_accuracy because bullet_accuracy already reset when sship.lives < 0
        
    def display_high_score(self, high_score, score):
        """
        sig: int, int --> int
        displays high score (points and waves completed) during title screen and game over
        must pass sship.high_score and sship.score, must set function = sship.high_score
        """
        if high_score < score:
            high_score = score
            self.init_new_high_score = 1
        if self.max_waves_completed < self.waves_completed:
            self.max_waves_completed = self.waves_completed
        HIGH_SCORE_FONT = pygame.font.SysFont('keyboard', 20)
        HIGH_SCORE_FONT1 = pygame.font.SysFont('keyboard', 15)
        HIGH_SCORE_FONT2 = pygame.font.SysFont('keyboard', 30)


        HIGH_SCORE_TEXT = "HIGH SCORE" 
        HIGH_SCORE_TEXT1 = "LEVEL"
        HIGH_SCORE_TEXT1a = "POINTS"
        HIGH_SCORE_TEXT2 = str(self.max_waves_completed)
        HIGH_SCORE_TEXT2a = str(high_score)


        h = HIGH_SCORE_FONT.render(HIGH_SCORE_TEXT, 1, WHITE)
        h1 = HIGH_SCORE_FONT1.render(HIGH_SCORE_TEXT1, 1, WHITE)
        h1a = HIGH_SCORE_FONT1.render(HIGH_SCORE_TEXT1a, 1, WHITE)
        h2 = HIGH_SCORE_FONT2.render(HIGH_SCORE_TEXT2, 1, WHITE)
        h2a = HIGH_SCORE_FONT2.render(HIGH_SCORE_TEXT2a, 1, WHITE)

        gap = 30

        SCREEN.blit(h, ( X_SCRNSIZE/2 - h.get_width()/2 , 40 + 0 ))
        SCREEN.blit(h1, ( X_SCRNSIZE/2 - h1.get_width() - gap, 40 + h.get_height()))
        SCREEN.blit(h1a, ( X_SCRNSIZE/2 + gap, 40 + h.get_height()))
        SCREEN.blit(h2, ( X_SCRNSIZE/2 - h1.get_width()/2 - h2.get_width()/2 - gap, 40 + h.get_height() + h1.get_height()))
        SCREEN.blit(h2a, ( X_SCRNSIZE/2 + h1a.get_width()/2 - h2a.get_width()/2 + gap, 40 + h.get_height() + h1.get_height()))

        return high_score
    
    

    def get_initials(self):
        """
        sig: none --> str
        takes keyboard input and returns two initials typed
        """
        #TO DO
        #make two strings, one for the first initial, one for the second
        #somehow make first string be only one letter long and input go to second string upon next press but not straight to second string
        kp = pygame.key.get_pressed()   
        i = 97
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        #letter_pressed = 0
        
        if self.fix == True:
            #window paused
            if self.switch == 0:
                self.switch = 1
            else:
                self.switch = 0
            
            self.fix_time += 1
            if self.fix_time >= self.fix_delta_time:
                self.fix = False
        #ALMOST WORKS
        #cant enter two letters in a row, find some way to iterate through and change barrier switches if last_i becomes False at any time (i.e. key lifted)
        if kp[self.last_i] == False:
            self.barrier_switch = 0
         
        if kp[self.last_i_2] == False:
            self.barrier_switch_2 = 0
        
        
        while i < 123:
            if kp[i] == True and kp[self.last_i] == False:
                if self.fix_time < self.fix_delta_time:
                    self.fix = True           
            else:            
                if self.fix == False:
                    self.fix_time = 0  
            
            if kp[i] == True:       
                if self.switch == 0:
                    if self.barrier_switch_2 == 0:
                        self.initial_1 = alphabet[i - 122 - 1].upper()
                        self.last_i = i
                        self.barrier_switch = 1
                        break
                else:
                    if self.barrier_switch == 0:
                        self.initial_2 = alphabet[i - 122 - 1].upper()
                        self.last_i_2 = i
                        self.barrier_switch_2 = 1
                        break
            
            i += 1
        return self.initial_1 + self.initial_2
    
    
    
    def store_high_scores(self, high_score, initials_length):
        
        """
        sig: int, int --> int
        stores high score (points and waves completed) in high_scores.txt file 
        must pass sship.high_score and sship.score, must set function = sship.high_score
        """

        #os.chdir(os.path.join('/Users','jeremyzay','Desktop','PythonProjects','Asteroids II', 'Assets', 'TextFiles'))
        #kp = pygame.key.get_pressed()        
        #getting input characters using kp dict
        #need to determine if pts or waves
        
        FONT = pygame.font.SysFont('keyboard', 40)
        TEXT = 'ENTER INITIALS'
        text_var = FONT.render(TEXT, 1, WHITE)
        
        """if str(high_score).isdigit() == False:
            high_score = 0
        if high_score < score:
            """
            
        """  f = open(os.path.join('Asteroids II', 'Assets', 'TextFiles', 'high_scores.txt'),'r')
        file_length = 0
        for line in f:
            file_length += 1
            line_hs = line
            

        #if len(self.initial_1) == 2:
        f = open(os.path.join('Asteroids II', 'Assets', 'TextFiles', 'high_scores.txt'),'w')

        i = 0
        while i < file_length + 1:
            if file_length > 0:
                f.write(line_hs)
            else:
                f.write(self.initial_1+self.initial_2+":"+str(high_score)+"\n")
            i += 1"""
        line_high_score = ""
        try:
            f = open(os.path.join('Asteroids II', 'Assets', 'TextFiles', 'high_scores.txt'),'r')
        
            for line in f:
                line_high_score += line

            line_hs_acc = ""
            for char in line_high_score:
                if char != "%":
                    line_hs_acc += char
                else:
                    self.hs_acc += line_hs_acc+"-"
            
            f = open(os.path.join('Asteroids II', 'Assets', 'TextFiles', 'high_scores.txt'),'w')
            hs_initials_value = ""
            #if len(self.initial_1 + self.initial_2) == 0:
            
            if len(initials_length) == 2:
                hs_initials_value = initials_length+":"+str(high_score)+"%"
                self.initial_start = 1

            """NOW ACTUALLY WORKS!!!!
           figure out faster way to debug (die faster, get score using keyboard commands, display var's on screen)"""
            
            """NEXT:
            STORE WAVES HIGH SCORE: just add it to hs_initials_value when triggered, have separating character
            separating character key:
            : leads to score high score
            - leads to initials (except for first one, potential bug) maybe don't need this, use isalpha? how to know which initials correspond to which high scores (will need loop with trigger when high score collected to collect initials, then to overwrite those iniitials if high score overwritten)
            % is end of line, triggers new score to be added (or something)
            ; WILL lead to waves high score
            WILL HAVE TO DISPLAY THE HIGH SCORES ALONG WITH THE INITIALS CORRESPONDING WITH THEM SOMEHOW SOMETIME (during game over screen and title screen?)"""  
                
            f.write(self.hs_acc + hs_initials_value)
            f.close()
        except FileNotFoundError:
            f = open(os.path.join('Asteroids II', 'Assets', 'TextFiles', 'high_scores.txt'),'w')
            #f.write(self.initial_1+self.initial_2+":"+str(high_score)+"%")
            f.close()

        #self.name_points = self.initial_1
        #self.initial_1 = 
        #return high_score
    
    
    
    
    
    def store_waves_high_score(self, event):
        os.chdir(os.path.join('/Users','jeremyzay','Desktop','PythonProjects','Asteroids II', 'Assets', 'TextFiles'))
        #kp = pygame.key.get_pressed()        
        #getting input characters using kp dict
        #need to determine if pts or waves
        
        FONT = pygame.font.SysFont('keyboard', 40)
        TEXT = 'ENTER INITIALS'
        text_var = FONT.render(TEXT, 1, WHITE)
        
        if self.max_waves_completed < self.waves_completed:
            
            if len(self.current_name_waves) < 2:
                SCREEN.blit(text_var, (X_SCRNSIZE/2, Y_SCRNSIZE/2))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        alphabet = "abcdefghijklmnopqrstuvwxyz"
                        #for letter in alphabet:
                        #initial = "K_"+letter
                        if 97 <= event.key <= 122:
                            initial = alphabet[event.key - 122 - 1]
                            self.current_name_waves += initial.upper()
            else:
                self.max_waves_completed = self.waves_completed
        f = open("high_scores.txt", "w")
        if len(self.current_name_waves) == 2:
            f.write("POINTS="+self.current_name_waves+":"+str(self.max_waves_completed)+"\n")
            self.name_waves = self.current_name_waves
            self.current_name_waves = ""
        f.close()
        
        
    
    #create_light_data()

        
    """def display_waves_completed(self):
        #NOT USED
        
        WAVES_FONT = pygame.font.SysFont('keyboard', 20)
        WAVES_FONT1 = pygame.font.SysFont('keyboard', 30)

        WAVES_TEXT = "WAVES" 
        WAVES_TEXT1 = str(self.waves_completed)
        w = WAVES_FONT.render(WAVES_TEXT, 1, WHITE)
        w1 = WAVES_FONT1.render(WAVES_TEXT1, 1, WHITE)
        SCREEN.blit(w, ( 60 - w.get_width()/2 , 40 + 0 ))
        SCREEN.blit(w1, ( 60 - w1.get_width()/2 , 40 + w.get_height()))
    """
    
    def display_score(self, score):
        """
        sig: int --> none
        displays player score
        must pass sship.score
        """
        SCORE_FONT = pygame.font.SysFont('keyboard', 50)

        score_text = SCORE_FONT.render( str(score), 1, WHITE)
        SCREEN.blit(score_text, ((X_SCRNSIZE - score_text.get_width() - 40), (score_text.get_height() - 30)))

    def display_waves_completed(self):
        """
        sig: none --> none
        displays waves completed
        """
        WAVES_FONT = pygame.font.SysFont('keyboard', 50)

        waves_text = WAVES_FONT.render( str(self.waves_completed), 1, WHITE)
        SCREEN.blit(waves_text, ((40 ), (waves_text.get_height() - 30)))

    def display_wave(self, spaceship):
        """
        sig: Spaceship --> none
        when triggered (new game started or new wave begins), displays text that fades in and then out, telling what wave on
        must pass sship object
        """
        if spaceship.restart_counter_initiate == 1:
            self.init_wave_display = 1
        if spaceship.lives < 0 or spaceship.lives == 0 and spaceship.destroy_spaceship == 1:
            self.init_wave_display = 0
            self.init_wave_color_decrease = 0
            self.wave_color_counter = 0
        
            
        max_wave_color_counter = 100
        
        if self.init_wave_display == 1:
            if spaceship.paused_true == 0:
                if self.init_wave_color_decrease == 0:
                    if self.wave_color_counter < max_wave_color_counter:
                        self.wave_color_counter += 1
                    else:
                        self.init_wave_color_decrease = 1
                else:
                    if self.wave_color_counter > 0:
                        self.wave_color_counter -= 1
                    else:
                        self.init_wave_color_decrease = 0
                        self.init_wave_display = 0
            
        
            
        wave_color_counter_factor = self.wave_color_counter/max_wave_color_counter
        wave_grayness = 220
        
        WAVE_FONT = pygame.font.SysFont('keyboard', 150)
        WAVE_TEXT = "LEVEL " + str(self.waves_completed)
        
        wave_color = wave_color_counter_factor * (255 - wave_grayness), wave_color_counter_factor * (255 - wave_grayness), wave_color_counter_factor * (255 - wave_grayness)
        draw_text_wave = WAVE_FONT.render(WAVE_TEXT, 1, wave_color)
        if self.init_wave_display == 1:
            SCREEN.blit(draw_text_wave, (X_SCRNSIZE/2 - draw_text_wave.get_width() / 2, Y_SCRNSIZE/2 - draw_text_wave.get_height() / 2))
        