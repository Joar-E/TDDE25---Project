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


#-- Initialise the display
pygame.init()

#width, height = pygame.display.get_surface().get_size()
pos_x = int(pygame.display.get_desktop_sizes()[0][0]/2 - 200)#- (width/2))
pos_y = int(pygame.display.get_desktop_sizes()[0][1]/2 - 200)#- (height/2))
def dynamicwinpos(x = pos_x, y = pos_y):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)



dynamicwinpos()
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


skip_update = 0
main_clock = pygame.time.Clock()

#-- Constants
FRAMERATE = 50
# These are later assigned a constant value
SINGLEPLAYER = False
MULTIPLAYER= False
#COOLDOWN_FOR_BULLET = 0

#-- Variables
running = False
game_mode_menu = False
start_menu = True
menu = True
current_mode = "Multiplayer"

#   Define the current level
current_map         = maps.map0
#   List of all game objects
game_objects_list   = []
tanks_list          = []
ai_list             = []


#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)

#-- Creating and rendering fonts
width = screen.get_width()
height = screen.get_height()
font = pygame.font.SysFont("arialblack", 25)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
dark_red = (90, 0, 0)
menu_color = (110, 110, 110)
button_color = (70, 70, 70)
b_hover_color = (40, 40, 40)
# smallfont = pygame.font.SysFont('Open Sans',34)
# smallerfont = pygame.font.SysFont('Open Sans',32)
# start_text = smallfont.render('Start game' , True , (255, 255, 255))
# game_mode_text = smallerfont.render('Gamemode', True, (255,255,255))
# quit_text = smallfont.render('Quit', True, (255,255,255))
# pygame.display.set_caption("Start Menu")

play_button = button.Button(100, 50, width/2, 50, button_color, b_hover_color)
game_mode_button = button.Button(100, 50, width/2, 150, button_color, b_hover_color)
quit_button = button.Button(100, 50, width/2, 250, button_color, b_hover_color)
back_button = button.Button(100, 50, width/2, height/2, button_color, b_hover_color)
single_player_button = button.Button(100, 50, width/3, 100, button_color, b_hover_color)
hot_seat_mult_button = button.Button(100, 50, width*2/3, 100, button_color, b_hover_color)

#Creates a start menu
# start_menu = True
# while start_menu:
    
#     screen.fill((255, 255, 255))
#     pygame.draw.rect(screen, (10,10,10),[width/4,height/4,width/2,height/7])
#     pygame.draw.rect(screen, (10,10,10),[width/4,(height/4) + 65 ,width/2,height/7])
#     pygame.draw.rect(screen, (10,10,10),[width/4,(height/4) + 130 ,width/2,height/7])
#     screen.blit(start_text , (width/4,height/4)) 
#     screen.blit(game_mode_text , (width/4,height/4 + 65)) 
#     screen.blit(quit_text , ((width/4) + 50,height/4 + 130)) 
#     pygame.display.update()
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#         if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == pygame.MOUSEBUTTONDOWN:
#             start_menu = False
#             pygame.mixer.music.play(-1)
#             pygame.display.set_caption("Capture The Flag")
#             running = True



while menu:
    if start_menu:
        pygame.display.set_caption("Main menu")
        screen.fill(menu_color)

        play_button.draw(screen, "Play", font, white)
        game_mode_button.draw(screen, "Game mode", font, white)
        quit_button.draw(screen, "Quit", font, white)

        if play_button.click():
            start_menu = False
            menu = False
            pygame.display.set_caption("Capture The Flag")
            running = True

        if game_mode_button.click():
            start_menu = False
            game_mode_menu = True

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

        # pygame.display.update()    
        # main_clock.tick(60)

    if game_mode_menu:
        pygame.display.set_caption("Main menu")
        screen.fill(menu_color)

        single_player_button.draw(screen, "1 player", font, white)
        hot_seat_mult_button.draw(screen, "2 players", font, white)
        back_button.draw(screen, "Back", font, white)

        # textobject = font.render(f"Current mode: {current_mode}", 1, white)
        # textrect = textobject.get_rect()
        # textrect.center = (width/2, height - 20)
        # screen.blit(textobject, textrect)
        button.Button.write_text(screen, f"Current mode: {current_mode}", font, white, width/2, height - 20)

        if single_player_button.click():
            SINGLEPLAYER = True
            MULTIPLAYER = False
            current_mode = "Single Player"

        if hot_seat_mult_button.click():
            MULTIPLAYER = True
            SINGLEPLAYER = False
            current_mode = "Multiplayer"

        if back_button.click():
            start_menu = True
            game_mode_menu = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_mode_menu = False
                    start_menu = True

    pygame.display.update()    
    main_clock.tick(FRAMERATE)

# Provided no arguments the default mode is multiplayer
if not SINGLEPLAYER or MULTIPLAYER:
    MULTIPLAYER = True

#-- Generate the background
background = pygame.Surface(screen.get_size())

#   Copy the grass tile all over the level area
for x in range(0, current_map.width):
    for y in range(0,  current_map.height):
        # The call to the function "blit" will copy the image
        # contained in "images.grass" into the "background"
        # image at the coordinates given as the second argument
        background.blit(images.grass,  (x*images.TILE_SIZE, y*images.TILE_SIZE))


#-- Create the boxes
def create_boxes():
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # Get the type of boxes
            box_type  = current_map.boxAt(x, y)
            # If the box type is not 0 (aka grass tile), create a box
            if(box_type != 0):
                # Create a "Box" using the box_type, aswell as the x,y coordinates,
                # and the pymunk space
                box = gameobjects.get_box_with_type(x, y, box_type, space)
                game_objects_list.append(box)
create_boxes()

#-- Create the flag
flag = gameobjects.Flag(current_map.flag_position[0], current_map.flag_position[1])
game_objects_list.append(flag)

#-- Create the bases
for i in range(0, len(current_map.start_positions)):
    position = current_map.start_positions[i]
    base = gameobjects.GameVisibleObject(position[0], position[1], images.bases[i])
    game_objects_list.append(base)

#Creates barriers

static_body = space.static_body
barrier_list = [pymunk.Segment(static_body, (0, 0), (0, current_map.height), 0.0), 
pymunk.Segment(static_body, (0, current_map.height), (current_map.width, current_map.height), 0.0),
pymunk.Segment(static_body, (current_map.width, current_map.height), (current_map.width, 0), 0.0),
pymunk.Segment(static_body, (current_map.width, 0), (0, 0), 0.0)
]

space.add(*barrier_list)

#-- Create the tanks


# Loop over the starting poistion
for i in range(0, len(current_map.start_positions)):
    # Get the starting position of the tank "i"
    pos = current_map.start_positions[i]
    # Create the tank, images.tanks contains the image representing the tank
    tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space)
    # Add the tank to the list of tanks
    tanks_list.append(tank)
    game_objects_list.append(tank)
    # Make every tank except one ai 
    if SINGLEPLAYER:
        if i > 0:
            ai_tank = ai.Ai(tank, game_objects_list, tanks_list, space, current_map)
            ai_list.append(ai_tank)
    # Make every tank except two ai
    if MULTIPLAYER:
        if i > 1:
            ai_tank = ai.Ai(tank, game_objects_list, tanks_list, space, current_map)
            ai_list.append(ai_tank)

#-- Player dictionaries
player1 = {"Index": 0,
           pygame.K_UP: tanks_list[0].accelerate,
           pygame.K_DOWN: tanks_list[0].decelerate,
           pygame.K_LEFT: tanks_list[0].turn_left,
           pygame.K_RIGHT: tanks_list[0].turn_right,
           pygame.K_SPACE: tanks_list[0].shoot
           }

# vplayer1 = {
#            pygame.K_UP: (tanks_list[0].accelerate, tanks_list[0].stop_moving),
#            pygame.K_DOWN: (tanks_list[0].decelerate, tanks_list[0].stop_moving),
#            pygame.K_LEFT: (tanks_list[0].turn_left, tanks_list[0].stop_turning),
#            pygame.K_RIGHT: (tanks_list[0].turn_right, tanks_list[0].stop_moving),
#            pygame.K_SPACE: (tanks_list[0].shoot, False)
#            }

player2 = {"Index": 1,
           pygame.K_w: tanks_list[1].accelerate,
           pygame.K_s: tanks_list[1].decelerate,
           pygame.K_a: tanks_list[1].turn_left,
           pygame.K_d: tanks_list[1].turn_right,
           pygame.K_q: tanks_list[1].shoot
           }

# Add human players
if SINGLEPLAYER:
    player_list = [player1] 
if MULTIPLAYER:
    player_list = [player1, player2]


def tank_movement_handler(player_list):
    """ A function for controlling the playble tanks"""

    for player in player_list:
        tank = tanks_list[player["Index"]]
        if event.type == KEYDOWN:
            if event.key in player:
                if event.key == list(player)[-1]:
                    if tank.can_shoot():
                        game_objects_list.append(player.get(event.key)(space))
                else:
                    player.get(event.key)()
        
        if event.type == KEYUP:
            if event.key in {list(player)[1], list(player)[2]} :
                tank.stop_moving()
            if event.key in {list(player)[3], list(player)[4]} :
                tank.stop_turning()


def play_explosion_anim(bullet):
    """ Playes the explosion animation at the coordinates of the bullet"""
    game_objects_list.append(bullet.explosion(space))

    for obj in game_objects_list:
        if isinstance(obj, gameobjects.Explosion):
            if obj.stop:
                game_objects_list.remove(obj)


#-- Functions for collision handling
def collision_bullet_bullet(arb, space, data):
    """Handles collisions between tanks and bullets"""
    bullet1 = arb.shapes[0]
    bullet2 = arb.shapes[1]
    if bullet2.parent in game_objects_list:
        space.remove(bullet1, bullet1.body)
        game_objects_list.remove(bullet1.parent)

    if bullet2.parent in game_objects_list:
        space.remove(bullet2, bullet2.body)
        game_objects_list.remove(bullet2.parent)
    play_explosion_anim(bullet1.parent)
    return False


def collision_bullet_tank(arb, space, data):
    """Handles collisions between tanks and bullets"""
    bullet_shape = arb.shapes[0]
    tank = arb.shapes[1].parent

    if tank != bullet_shape.parent.tank:
        if bullet_shape.parent in game_objects_list:
            space.remove(bullet_shape, bullet_shape.body)
            game_objects_list.remove(bullet_shape.parent)
            play_explosion_anim(bullet_shape.parent)
            # If 2000 ticks have passed since tak respawn
            # check tank hit points
            if pygame.time.get_ticks() - tank.get_respawn_time() > 2500:
                # Remove 1 hp from the tank
                tank.decrease_hp()
                # If the tank has 0 hp respawn it
                if tank.get_hit_points() == 0:
                    # Save time of death
                    tank.set_respawn_time(pygame.time.get_ticks())
                    sounds.tank_shot_sound.play()
                    tank.respawn()
                    tank.drop_flag(flag)

    return False


def collision_bullet_box(arb, space, data):
    """Handles collisions between bullets and boxes"""
    bullet_shape = arb.shapes[0]
    box = arb.shapes[1]
    sounds.box_sound.set_volume(0.2)
    sounds.box_sound.play()
    if bullet_shape.parent in game_objects_list:
        space.remove(bullet_shape, bullet_shape.body)
        game_objects_list.remove(bullet_shape.parent)

        space.remove(box, box.body)
        game_objects_list.remove(box.parent)
        play_explosion_anim(bullet_shape.parent)
    return False


def ind_collision_bullet_box(arb, space, data):
    """Handels collisions between bullets and indestructable objects"""
    bullet_shape = arb.shapes[0]
    if bullet_shape.parent in game_objects_list:
        space.remove(bullet_shape, bullet_shape.body)
        game_objects_list.remove(bullet_shape.parent)
        play_explosion_anim(bullet_shape.parent)
    return False


bullet_bullet_c_handler = space.add_collision_handler(1, 1)
bullet_bullet_c_handler.pre_solve = collision_bullet_bullet

indestructible_c_handler = space.add_collision_handler(1, 0)
indestructible_c_handler.pre_solve = ind_collision_bullet_box

tank_c_handler = space.add_collision_handler(1, 2)
tank_c_handler.pre_solve = collision_bullet_tank

box_c_handler = space.add_collision_handler(1, 3)
box_c_handler.pre_solve = collision_bullet_box

#----- Main Loop -----#




#-- Control whether the game run

while running:
    for tank_ai in ai_list:
        tank_ai.decide()

    for tank in tanks_list:
            tank.try_grab_flag(flag)
            if tank.has_won():
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
                create_boxes()
                continue
                
                #running = False
    #-- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sounds.flag_sound.play()
            running = False
        
        tank_movement_handler(player_list)

        
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
   

    flag.update_screen(screen)
    
    
    #   Redisplay the entire screen (see double buffer technique)
    pygame.display.flip()

    #   Control the game framerate
    clock.tick(FRAMERATE)



