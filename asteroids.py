import pygame as pg
from sys import exit
import os
import math

#import random


#TO DO
#only allow next level to begin once all objects leave the screen
#have high scores (points and levels) saved in text file
#allow user to input initials to correspond with high score
#have moment when high scores display 1,2,3 with initials
#have new high score display
#spaceships



pg.display.init()
pg.font.init()
pg.mixer.init()


#IMPORT CLASSES

#import Constants.constants as constants
from Classes.Window import Window

from Classes.Spaceship4 import Spaceship
from Classes.Spaceship4 import SpaceshipLives
from Classes.Spaceship4 import SpaceshipAutomated
from Classes.Spaceship4 import SpaceshipAutomatedList

from Classes.Asteroid2 import Asteroid
from Classes.AsteroidList2 import AsteroidList

from Classes.Bullet import Bullet
from Classes.BulletList import BulletList

from Classes.Level3 import Level
#******************************************************* SOUND *******************************************************


#sound if ran from Asteroids_v2 folder:

bullet_fire = pg.mixer.Sound(os.path.join('Assets', 'AsteroidSounds', 'fire.wav'))
engine_sound = pg.mixer.Sound(os.path.join('Assets', 'AsteroidSounds', 'thrust1.wav'))
bip1 = pg.mixer.Sound(os.path.join('Assets', 'AsteroidSounds', 'beat1.wav'))
bip2 = pg.mixer.Sound(os.path.join('Assets', 'AsteroidSounds', 'beat2.wav'))

bang_sship_auto_destroy = pg.mixer.Sound(os.path.join('Assets', 'AsteroidSounds', 'bangSmall.wav'))
bang_ast_destroy = pg.mixer.Sound(os.path.join('Assets', 'AsteroidSounds', 'bangLarge.wav'))
bang_sship_destroy = pg.mixer.Sound(os.path.join('Assets', 'AsteroidSounds', 'bangMedium.wav'))



#BOOLEAN VALUES
run = True

bullet_fire_fix = False
pause_fix = False


clock = pg.time.Clock()

#******************************************************* CONSTANTS *******************************************************

#SCREEN
X_SCRNSIZE, Y_SCRNSIZE = 1200, 800
SCREEN = pg.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))

#FRAMES PER SECOND
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
ACCELERATION = 0.2
DECELERATION = 0.02
ROTATE = 5

RAD2DEG = 180 / math.pi
DEG2RAD = math.pi / 180

#SPACESHIP MOVEMENT
ACCELERATION = 0.25
DECELERATION = 0.1
ROTATE = 7


#Bullet firing and asteroid variables and constants

#NEXT TIMES
next_bullet_time = 0
next_spaceship_fire_time = 0
next_asteroid_time = 0
next_spaceship_time = 0
next_bullet_auto_time = 0
next_rocket_sound_time = 0

next_pause_time = 0

###KEY PRESS FIXES

#bullet fire spacebar fix
bullet_fire_fix_delta_time = 1
bullet_fire_fix_time = 0

#pause
pause_fix_delta_time = 1
pause_fix_time = 0

#DELTA TIMES:
#initial DELTA TIMES
initial_spaceship_fire_delta_time = 500 #increases
initial_asteroid_delta_time = 1200    
initial_spaceship_delta_time = 6000 
#dynamic DELTA TIMES
spaceship_fire_delta_time = initial_spaceship_fire_delta_time #increases
asteroid_delta_time = initial_asteroid_delta_time    
spaceship_delta_time = initial_spaceship_delta_time 
#static DELTA TIMES
bullet_delta_time = 150
rocket_sound_delta_time = 285 #ticks of rocket sound
pause_delta_time = 500

#MINIMUM DELTA TIMES:
min_asteroid_delta_time = 450
min_spaceship_delta_time = 2500
max_spaceship_fire_delta_time = 1500

#LEVEL FACTORS

#COUNTERS

initial_next_level_time = 50
next_level_time = initial_next_level_time
level_delta_time = 1000

#delay_spawning = 0 #finicky

phase_1_trigger = 0
phase_2_trigger = 0
phase_3_trigger = 0


#BULLET MOVEMENT
MAX_BULLETS = 100
bullet_speed = 20
#auto_bullet_speed = 5



#******************************************************* OBJECTS *******************************************************

#create spacecraft
sship = Spaceship(WHITE, X_SCRNSIZE/2, Y_SCRNSIZE/2, 20, 0, 0, 0)

#create spacecrafts that tell how many livese remaining
sship1 = SpaceshipLives(WHITE, 60, 60, 20, 0, 0, 0)
sship2 = SpaceshipLives(WHITE, 100, 60, 20, 0, 0, 0)
sship3 = SpaceshipLives(WHITE, 140, 60, 20, 0, 0, 0)

#create lists of objects (asteroids, bullets, automated spaceships)
asteroid_collection = AsteroidList()
bullet_collection = BulletList()
sship_collection = SpaceshipAutomatedList()

#object Bip: handles timing of bips
level = Level()

#removed this because there should only be one bullet list, more efficient

#if want to use info from other classes, create undefined variable (that needs to be passed) and then when initiating object/method, pass variable from other class

#create window
window = Window()

pause = False
#******************************************************* MAIN *******************************************************

while run:
    window.display()

    clock.tick(FPS)
    current_time = pg.time.get_ticks()
    level.main_counter += 1
    
    kp = pg.key.get_pressed()        

    for event in pg.event.get():
        if event.type == pg.QUIT or kp[pg.K_q] == True:
            pg.quit()
            exit()    
            
    #make cursor invisible when playing game
    if sship.lives < 0 or window.paused == 1:
        pg.mouse.set_visible(1)
    else:
        pg.mouse.set_visible(0)
    
    # if level.init_new_high_score == 1:
    #     window.display_debug_value(level.get_initials(), (X_SCRNSIZE/2, Y_SCRNSIZE/2))

    #     # level.store_high_scores(sship.high_score, "JZ")
    #     if len(level.get_initials()) == 2:    
            
    #         level.init_new_high_score = 0
    #first note is broken, plays both at once, then fixes
    
    #reset bips if all phases complete (is it level.main_counter or level_counter? when does level_counter exist?)

    level.display_wave(sship)
    #restart game
    if sship.destroy_spaceship == 1:
        pass
        #sship_destroyed_counter = bip_level_counter
        
        #next_bip1_sound = next_bip2_sound = bip_level_counter + bip_sound_delta_time


    

    level.level_counter = level.main_counter - level.restart_counter - level.pause_counter_adjust# - level.sship_destroyed_counter_reset
    
    
    #need to fix bip phases resetting on destroyed spaceships (fixed badly) and on reset
    #should be based off of function, not redefining bip phase values every time
    #figure out what level.bip_phases_completion_counter should = (the bip phase function (below) isn't initiating upon death/reset)

    if sship.lives >= 0:
        level.bip_counters_phases_increase()

    #level.current_sship_lives = sship.lives
    if sship.lives == 0 and level.current_sship_lives == 0:
        #cause restart_counter_init if sship has no lives remaining (this is placeholder code)
        level.sship_destroyed_counter_reset = level.level_counter
        level.current_sship_lives = 1
    if sship.lives == 1:
        level.current_sship_lives = 0
        
    level.reset_counters(sship)
    level.bip_restart_counters()
    
    bullet_collection.bullet_accuracy = level.next_difficulty_wave(bullet_collection.bullet_accuracy)

  
    #make copy of asteroid display; rename; instead of generating circle, generate polygon; generate random number between min radius and max radius; plot number around radius every # degrees in a circle
    #game over after spaceship hit 3 times

    
    
    #score (stored in method check_if_bullets_hit: outputs a value depending on what the bullets hit)
    sship.score = sship.score + bullet_collection.check_if_bullets_hit(asteroid_collection) + bullet_collection.check_if_bullets_hit(sship_collection)




    if window.paused == 0:
        
        if sship.destroy_spaceship == 0:   
            #add new asteroid
            if level.level_counter == level.next_asteroid_time:
                ast = Asteroid(WHITE, X_SCRNSIZE/3, Y_SCRNSIZE/3, 25, 20, 180)
                ast.generate_random()
                asteroid_collection.append( ast )
                
                level.next_asteroid_time = level.level_counter + int(level.asteroid_delta_time)
            
            
            #add new spaceships
            #FIXED, but has issues, cant specify start time of when sships start getting appended
            if level.level_counter == level.next_spaceship_time:
                #add new spaceship
                #PROBLEM: sship_auto only desplays when speed is 10
                sship_auto = SpaceshipAutomated(RED, 0, 0, 40, 2, 90, 0)
                sship_auto.generate_random()
                sship_collection.append( sship_auto )
                
                level.next_spaceship_time = level.level_counter + int(level.spaceship_delta_time)


            #fire bullets from automated spaceships
            if level.level_counter == level.next_spaceship_fire_time:
                #fire automated spaceships
                bullet_collection.fire_automated_bullets( sship_collection, sship )
                level.next_spaceship_fire_time = level.level_counter + int(level.spaceship_fire_delta_time)
        else:
            level.next_asteroid_time = level.next_spaceship_time = level.next_spaceship_fire_time = level.level_counter + level.offset

        #increase DELTA TIMES
        """if sship.game_over_true == 0 and sship.lives >= 0:
            if level.level_counter == next_level_time:

                #increase/decrease DELTA TIMES as levels increase:
                if asteroid_delta_time > min_asteroid_delta_time:
                    asteroid_delta_time = asteroid_delta_time * factor_asteroid_delta_time
                
                if spaceship_delta_time > min_spaceship_delta_time:
                    spaceship_delta_time = spaceship_delta_time * factor_spaceship_delta_time
                
                if spaceship_fire_delta_time < max_spaceship_fire_delta_time:
                    spaceship_fire_delta_time = spaceship_fire_delta_time * factor_spaceship_fire_delta_time

                if bullet_collection.bullet_accuracy >= 0:
                    bullet_collection.bullet_accuracy = bullet_collection.bullet_accuracy * factor_bullet_accuracy
                
                #sship_auto.color_change = sship_auto.color_change * factor_color_change/5 #PROBLEM: every time a new sship_auto is created, the color_change is reset to the init value

                next_level_time = level.level_counter + level_delta_time"""

        if sship.game_over_true == 0 and sship.lives >= 0:
            bullet_collection.bullet_accuracy = level.increase_delta_times(bullet_collection.bullet_accuracy)
            #phases sounds
            #phase 1
            #find a way to set #'d bip counters back to zero upon spaceship destroyed
            level.bip_sound(sship)
            level.bip_phases_increase()
            #create counter when sship invulnerable, when counter = 1, reset bip counters (subtracted value from bip counter earlier, = bip counter at that moment, to make it 0)
            #INCORRECT: want bip_counters and phases to reset only when new game initiated, NOT when sship destroyed
            #level.sship_respawn_func()

            #level.bip12_counter_reset_func()

        #move asteroids
        asteroid_collection.move_asteroids()
        
        #check if objects hit bullets
        asteroid_collection.check_if_asteroids_hit(bullet_collection)
        sship_collection.check_if_spaceships_hit(bullet_collection)

        #split asteroids
        asteroid_collection.split_asteroids()

        #delete hit objects
        asteroid_collection.delete_hit_asteroids()
        sship_collection.delete_hit_spaceships()
        bullet_collection.delete_hit_bullets()

        #move bullets
        bullet_collection.move_bullets()

        #move sship
        if sship.game_over_true == 0 and sship.lives >= 0:
            sship.move()
        #fire bullets

        if bullet_fire_fix == True:
            if len(bullet_collection) < MAX_BULLETS and current_time >= next_bullet_time and sship.destroy_spaceship == 0 and sship.game_over_true == 0 and sship.lives >= 0:
                bullet = Bullet(sship, bullet_speed, sship.orientation, 1)
                bullet_collection.append(bullet)
                #bullet.manned_spaceship = 1
                bullet_fire.play()
                next_bullet_time = current_time + bullet_delta_time                
                #spacebar shoots only once
                bullet_fire_fix_time += 1
                if bullet_fire_fix_time >= bullet_fire_fix_delta_time:
                    #bullet_fire_fix_time = 0
                    bullet_fire_fix = False
        #spacebar shoots only once
        if kp[pg.K_SPACE]:
            if len(bullet_collection) < MAX_BULLETS and current_time >= next_bullet_time and sship.destroy_spaceship == 0 and sship.game_over_true == 0 and sship.lives >= 0:
                if bullet_fire_fix_time < bullet_fire_fix_delta_time:
                    bullet_fire_fix = True           
        else:            
            if bullet_fire_fix == False:
                bullet_fire_fix_time = 0
            
            
        #rocket sound
        if kp[pg.K_UP]:
            #engine_sound.play()
            if current_time >= next_rocket_sound_time and sship.destroy_spaceship == 0 and sship.game_over_true == 0 and sship.lives >= 0:
                #add new spaceship
                #FIXED **** PROBLEM: sship_auto only desplays when speed is 10 
                engine_sound.play()
                next_rocket_sound_time = current_time + rocket_sound_delta_time

        #move auto sships
        sship_collection.move_spaceships()
    else:
        level.pause_counter_adjust += 1

        

    #display asteroids
    asteroid_collection.display_asteroids(SCREEN)

    #display auto spaceships
    sship_collection.display_spaceships()
    
    #display bullets
    bullet_collection.display_bullets()

    

    sship.invulnerable()
    #Display Spaceship
    if sship.lives >= 0:
        if sship.invulnerability == 0:
            if sship.check_distance(asteroid_collection) == 1 or sship.check_distance( sship_collection ) == 1 or sship.check_distance( bullet_collection ) == 1:
                sship.destroy_spaceship = 1

    
        if sship.destroy_spaceship == 1:
            sship.destroy()
            #destroy_score_increase = 1

        else:
            sship.display()
   

    if sship.lives == 0: 
        if sship.destroy_counter > (sship.end_destroy_counter/2):
            sship.game_over_true = 1
    if sship.game_over_true == 1:
        sship.game_over()
    if sship.lives <= -1:
        sship.restart_lives1(event)
        sship.high_score = level.display_high_score(sship.high_score, sship.score)
        #sship.high_score = level.store_high_scores(event, sship.high_score, sship.score)
        level.display_waves_completed()
        sship3.revert_spaceship3()
        sship2.revert_spaceship2()
        sship1.revert_spaceship1()
        bullet_collection.bullet_accuracy = 180


    #new spaceships slot in (doesn't work with pause, so I got lazy and removed it)
    """if sship.lives == 3 and sship.destroy_spaceship == 1:
        sship3.get_new_spaceship3()
    if sship.lives == 2 and sship.destroy_spaceship == 1:
        sship2.get_new_spaceship2()
    if sship.lives == 1 and sship.destroy_spaceship == 1:
            sship1.get_new_spaceship1()
    """

    if sship.refresh_screen == 1:
        #asteroid_collection.refresh_screen_asteroids()
        asteroid_collection.clear()
        bullet_collection.clear()
        sship_collection.clear()
        sship.refresh_screen = 0


    if sship.lives == 3:
        sship3.display()
    if sship.lives >= 2:
        sship2.display()
    if sship.lives >= 1:
        sship1.display() 
    

    
    sship.score_display()
    if sship.lives == -2:
        window.title_screen()
        window.signature()
        sship.reset_counters()
    
    #SSHIP AND ASTEROID SOUND
    if sship.game_over_true == 0 and sship.lives >= 0:
        if asteroid_collection.asteroid_destroy_sound_play == 1:
            bang_ast_destroy.play()
            asteroid_collection.asteroid_destroy_sound_play = 0
        if sship_collection.spaceship_auto_destroy_sound_play == 1:
            bang_sship_auto_destroy.play()
            sship_collection.spaceship_auto_destroy_sound_play = 0
        if sship.spaceship_destroy_sound_play == 1:
            bang_sship_destroy.play()
            sship.spaceship_destroy_sound_play = 0
    else:
        asteroid_collection.asteroid_destroy_sound_play = 0
        sship_collection.spaceship_auto_destroy_sound_play = 0
        sship.spaceship_destroy_sound_play = 0

    
    #TOGGLE AUTOMATED SPACESHIP ACCURACY: 
    #doesn't work very well (works, just not reliable)
    #bullet_collection.toggle_bullet_accuracy(event)
    #bullet_collection.display_bullet_accuracy()
    
    """if kp[pg.K_a]:
        bullet_collection.bullet_accuracy = 0
    """
    #if sship.lives >= 0 and sship.game_over_true == 0 and sship.destroy_spaceship == 0 and sship.invulnerability_counter == 0:
    if sship.lives >= 0 and sship.game_over_true == 0:

        if pause_fix == True:
            #window paused
            if window.paused == 0:
                window.paused = 1
            else:
                window.paused = 0
            
            pause_fix_time += 1
            if pause_fix_time >= pause_fix_delta_time:
                pause_fix = False
    

        if kp[pg.K_p]:
            if pause_fix_time < pause_fix_delta_time:
                pause_fix = True           
        else:            
            if pause_fix == False:
                pause_fix_time = 0

    if window.paused == 1:
        window.pause()
        sship.paused_true = 1
        

        
        if kp[pg.K_r]:
            sship.lives = -2
            sship.x_coord = X_SCRNSIZE/2
            sship.y_coord = Y_SCRNSIZE/2
            sship.orientation = 0
            sship.speed = 0
            window.paused = 0
        
    else:
        
        sship.paused_true = 0

    #DEBUG DISPLAYS
    """
    #counters
    window.display_debug_value(level.level_counter, (20, Y_SCRNSIZE-50))
    window.display_debug_value(level.restart_counter, (20, Y_SCRNSIZE-100))
    #bip phasesq
    window.display_debug_value(level.waves_completed, (20, Y_SCRNSIZE - 150))
    window.display_debug_value(level.bip_delta_time_factor, (60, Y_SCRNSIZE - 150))
    #sship lives
    #window.display_debug_value(sship.lives, (80, Y_SCRNSIZE-50))
    #delta times
    window.display_debug_value(int(level.asteroid_delta_time), (20, Y_SCRNSIZE - 200))
    window.display_debug_value(int(bullet_collection.bullet_accuracy), (20, Y_SCRNSIZE - 250))
    #next times
    window.display_debug_value(level.next_level_time, (20, Y_SCRNSIZE - 300))
    #phases
    window.display_debug_value(level.bip_phase_3 - level.bip_phase_1, (20, Y_SCRNSIZE - 400))
    #difficulty
    window.display_debug_value(level.difficulty_level, (20, Y_SCRNSIZE - 350))
    #trigger values
    #window.display_debug_value(sship.restart_counter_initiate, (20, Y_SCRNSIZE - 300))
    window.display_debug_value(int(level.next_asteroid_time), (20, Y_SCRNSIZE - 450))
    """
    """try:
        window.display_debug_value("Initials-"+level.get_initials(), (20, Y_SCRNSIZE-50))
    except TypeError:
        window.display_debug_value("None", (20, Y_SCRNSIZE-50))
    window.display_debug_value(level.switch, (20, Y_SCRNSIZE-100))
    """


    


    
    


    pg.display.update()
 

    
    if kp[pg.K_b]:
        breakpoint()
        
pg.quit()