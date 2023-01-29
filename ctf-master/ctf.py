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
current_mode = "Singleplayer"
current_map_string = "Map 1"

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


#-- Create the screen and the the surface which sice will depend on the current map
#-- Also defines the screenoffset so that the game screen always is at the center of the screen
menu_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.Surface(current_map.rect().size)
screen_offset = tuple([(x[0]-x[1])/2 for x in zip( menu_screen.get_size(), screen.get_size() )])


#-- Creating and rendering fonts and colours
width = menu_screen.get_width()
height = menu_screen.get_height()
font = pygame.font.SysFont("arialblack", 50)
white = (255, 255, 255)
menu_colour = (60, 60, 60)
button_colour = (120, 120, 120)
b_hover_colour = (40, 40, 40)


#Creates the buttons

#--Start menu buttons
play_button = button.Button(200, 100, width/2, height/4,
                            button_colour, b_hover_colour, 
                            "Play", font, white)

settings_button = button.Button(300, 100, width/2, height/2,
                                button_colour, b_hover_colour, 
                                "Settings", font, white)

quit_button = button.Button(200, 100, width/2, height*3/4,
                            button_colour, b_hover_colour, 
                            "Quit", font, white)

#--Settings menu buttons
game_mode_button = button.Button(400, 100, width/2, height/2, 
                                 button_colour, b_hover_colour, 
                                 "Game Modes", font, white)

map_button = button.Button(450, 100, width/2, height/4, 
                           button_colour, b_hover_colour, 
                           "Map Selection", font, white)

back_button = button.Button(200, 100, width/2, height*3/4, 
                            button_colour, b_hover_colour, 
                            "Back", font, white)

#--GameMode menu buttons
single_player_button = button.Button(400, 100, width/3, height/4, 
                                     button_colour, b_hover_colour, 
                                     "Singleplayer", font, white)

hot_seat_mult_button = button.Button(400, 100, width*2/3, height/4, 
                                     button_colour, b_hover_colour, 
                                     "Multiplayer", font, white)

#--Map menu buttons
map1_button = button.Button(200, 100, width/4, height/4,
                            button_colour, b_hover_colour, 
                            "Map 1", font, white)

map2_button = button.Button(200, 100, width/2, height/4,
                            button_colour, b_hover_colour, 
                            "Map 2", font, white)

map3_button = button.Button(200, 100, width*3/4, height/4, 
                            button_colour, b_hover_colour, 
                            "Map 3", font, white)


#Creates a start menu


while menu:
    # Creates the start menu and handles its events
    if start_menu:
        pygame.display.set_caption("Main menu")
        menu_screen.fill(menu_colour)

        play_button.draw(menu_screen)
        settings_button.draw(menu_screen)
        quit_button.draw(menu_screen)

        if play_button.click():
            menu_screen.fill(menu_colour)
            start_menu = False
            menu = False
            pygame.display.set_caption("Capture The Flag")
            running = True

        if settings_button.click():
            start_menu = False
            settings_menu = True

        if quit_button.click():
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Creates the settings menu and handles its events
    if settings_menu:
        pygame.display.set_caption("Settings")
        menu_screen.fill(menu_colour)

        game_mode_button.draw(menu_screen)
        map_button.draw(menu_screen)
        back_button.draw(menu_screen)

        if game_mode_button.click():
            settings_menu = False
            game_mode_menu = True
        
        if map_button.click():
            settings_menu = False
            map_menu = True
        
        if back_button.click():
            settings_menu = False
            start_menu = True
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    start_menu = True
                    settings_menu = False

    #Creates the game_mode_menu and handles its events
    if game_mode_menu:
        pygame.display.set_caption("Game-mode menu")
        menu_screen.fill(menu_colour)

        single_player_button.draw(menu_screen)
        hot_seat_mult_button.draw(menu_screen)
        back_button.draw(menu_screen)

        button.Button.write_text(menu_screen, f"Current mode: {current_mode}", 
                                 font, white, width/2, height/2)
        
        if single_player_button.click():
            singleplayer = True
            multiplayer = False
            current_mode = "Single Player"

        if hot_seat_mult_button.click():
            multiplayer = True
            singleplayer = False
            current_mode = "Multiplayer"

        if back_button.click():
            settings_menu = True
            game_mode_menu = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_mode_menu = False
                    settings_menu = True
    
    # Creates the map menu and handles its events
    if map_menu:
        pygame.display.set_caption("Map Selection")
        menu_screen.fill(menu_colour)

        map1_button.draw(menu_screen)
        map2_button.draw(menu_screen)
        map3_button.draw(menu_screen)
        back_button.draw(menu_screen)

        button.Button.write_text(menu_screen, 
                                 f"Current map: {current_map_string}", 
                                 font, white, width/2, height/2)

        button.Button.write_text(menu_screen, "9X9", font, white, 
                                 width/4, height/4 + 100)

        button.Button.write_text(menu_screen, "15X11", font, white,
                                 width/2, height/4 + 100)

        button.Button.write_text(menu_screen, "10X5", font, white, 
                                 width*3/4, height/4 + 100)

        if map1_button.click():
            current_map = maps.map0
            current_map_string = "Map 1"
            screen = pygame.Surface(current_map.rect().size)
            screen_offset = tuple([(x[0]-x[1])/2 for x in zip( menu_screen.get_size(), screen.get_size() )])

        if map2_button.click():
            current_map = maps.map1
            current_map_string = "Map 2"
            screen = pygame.Surface(current_map.rect().size)
            screen_offset = tuple([(x[0]-x[1])/2 for x in zip( menu_screen.get_size(), screen.get_size() )])

        if map3_button.click():
            current_map = maps.map2
            current_map_string = "Map 3"
            screen = pygame.Surface(current_map.rect().size)
            screen_offset = tuple([(x[0]-x[1])/2 for x in zip( menu_screen.get_size(), screen.get_size() )])
        
        if back_button.click():
            settings_menu = True
            map_menu = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    settings_menu = True
                    map_menu = False


    pygame.display.update()    
    main_clock.tick(FRAMERATE)

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



