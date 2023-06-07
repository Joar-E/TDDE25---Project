import os
import sys
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d
import math
import sounds
import button
#----- Initialisation -----#
# Initialize arg parser
mode = sys.argv[1:]


#-- Initialise the display
pygame.init()

pygame.display.set_mode()

#-- Initialise the clock
clock = pygame.time.Clock()

#-- Initialise the physics engine
space = pymunk.Space()
space.gravity = (0.0,  0.0)
space.damping = 0.1 # Adds friction to the ground for all objects


#-- Import from the ctf framework
import ai
import images
import gameobjects
import maps
import backgroundinit
import collisions
import playermovement
import mainmenu

skip_update = 0
main_clock = pygame.time.Clock()

#-- Constants
FRAMERATE = 50
SCREEN_RESOLUTION = (1360, 768)


#-- Variables
menu = True
start_menu = True
settings_menu = False
game_mode_menu = False
map_menu = False
running = False

singleplayer = False
multiplayer  = False
#   Define the current level
current_map         = maps.map0
#   List of all game objects
game_objects_list   = []
tanks_list          = []
ai_list             = []


# Player mode is determined
if mode == ['--singleplayer']:
    singleplayer = True
    current_mode = "Singleplayer"

if mode == ['--hot-multiplayer']:
    multiplayer = True
    current_mode = "Multiplayer"


#--- Show the start menu ---#
mainmenu.show_menu(main_clock, FRAMERATE)
# Update variables according to the players choices
screen, menu_screen, screen_offset = mainmenu.get_screen()
singleplayer, multiplayer = mainmenu.get_game_mode()
current_map = mainmenu.get_map()

# Menu is closed
running = True

# Provided no arguments the default mode is singleplayer
if not singleplayer and not multiplayer:
    singleplayer = True


#-- Generate the background
background = backgroundinit.create_background(current_map, screen)


#-- Create enviroment and flag
backgroundinit.create_enviroment(current_map, game_objects_list, space)
flag = backgroundinit.create_flag(current_map, game_objects_list)


#-- Create the tanks
def create_ai(tank):
    """Make tanks into AI"""
    ai_tank = ai.Ai(tank, game_objects_list, tanks_list, space, current_map)
    ai_list.append(ai_tank)


def create_tanks():
    """Creates tanks according to game mode and map"""
    # Loop over the starting poistion
    for i in range(0, len(current_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = current_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space, True)
        # Add the tank to the list of tanks
        tanks_list.append(tank)
        game_objects_list.append(tank)
        # Make every tank except one ai 
        if singleplayer:
            if i > 0:
                create_ai(tank)
        # Make every tank except two ai
        if multiplayer:
            if i > 1:
                create_ai(tank)
            
create_tanks()


# Add human players
player_list = \
    playermovement.add_players(tanks_list, singleplayer, multiplayer)


#-- Create collision handlers
bullet_bullet_c_handler = space.add_collision_handler(1, 1)
bullet_bullet_c_handler.pre_solve = \
    collisions.create_bullet_bullet_handler(game_objects_list, space)

indestructible_c_handler = space.add_collision_handler(1, 0)
indestructible_c_handler.pre_solve = \
    collisions.create_ind_box_handler(game_objects_list, space)


tank_c_handler = space.add_collision_handler(1, 2)
tank_c_handler.pre_solve = \
    collisions.create_bullet_tank_handler(game_objects_list, space, flag)

box_c_handler = space.add_collision_handler(1, 3)
box_c_handler.pre_solve = \
    collisions.create_bullet_box_handler(game_objects_list, space)


def reset_game(tank):
    sounds.victory_sound.play()
    # Add 1 to it's score
    tank.update_score()
    # Remove the flag
    tank.drop_flag(flag)
    # Relocate the flag
    flag.x = current_map.flag_position[0]
    flag.y = current_map.flag_position[1]
    
    # Respawn each tank and show their scores
    for index, tank in enumerate(tanks_list):
        tank.respawn()
        print(f"Player {index + 1}: {tank.get_score()}")
    print()
    for box in game_objects_list:
        # Find a wooden or iron box
        if type(box) == gameobjects.Box and \
        box.movable == True:
            # remove it from list and space
            game_objects_list.remove(box)
            space.remove(box.shape, box.body)
    # create new ones
    backgroundinit.create_boxes(current_map, game_objects_list, space)              


#----- Main Loop -----#


#-- Control whether the game run

while running:
    
    for tank_ai in ai_list:
        tank_ai.decide()

    for tank in tanks_list:
            tank.try_grab_flag(flag)
            if tank.has_won():
                reset_game(tank)
                continue
                
                #running = False
    #-- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sounds.flag_sound.play()
            running = False
        
        playermovement.tank_movement_handler(player_list, game_objects_list,
                                            tanks_list, event, space)

        
    #-- Update physics
    if skip_update == 0:
        # Loop over all the game objects and update their speed in function of their
        # acceleration.
        for obj in game_objects_list:
            obj.update()
        skip_update = 2
    else:
        skip_update -= 1


    #   Check collisions and update the objects position
    space.step(1 / FRAMERATE)

    #   Update object that depends on an other object position (for instance a flag)
    for obj in game_objects_list:
        obj.post_update()

    #-- Update Display

    
    # Display the background on the screen
    screen.blit(background, (0, 0))

    
    # Update the display of the game objects on the screen
    for obj in game_objects_list:
        obj.update_screen(screen)

    #Shows the tanks on the screen
    for tank in tanks_list:
        tank.update_screen(screen)
   

    
    menu_screen.blit(screen, screen_offset)

    
    #   Redisplay the entire screen (see double buffer technique)
    pygame.display.flip()

    #   Control the game framerate
    clock.tick(FRAMERATE)



