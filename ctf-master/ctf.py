import os
import sys
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d
import math
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


#-- Constants
FRAMERATE = 50
#COOLDOWN_FOR_BULLET = 0

#-- Variables


#   Define the current level
current_map         = maps.map0
#   List of all game objects
game_objects_list   = []
tanks_list          = []
ai_list             = []



#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)
width = screen.get_width()
height = screen.get_height()
smallfont = pygame.font.SysFont('Open Sans',34)
smallerfont = pygame.font.SysFont('Open Sans',32)
start_text = smallfont.render('Start game' , True , (255, 255, 255))
game_mode_text = smallerfont.render('Gamemode', True, (255,255,255))
quit_text = smallfont.render('Quit', True, (255,255,255))
pygame.display.set_caption("Start Menu")

#Creates a start menu
start_menu = True
while start_menu:
    
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (10,10,10),[width/4,height/4,width/2,height/7])
    pygame.draw.rect(screen, (10,10,10),[width/4,(height/4) + 65 ,width/2,height/7])
    pygame.draw.rect(screen, (10,10,10),[width/4,(height/4) + 130 ,width/2,height/7])
    screen.blit(start_text , (width/4,height/4)) 
    screen.blit(game_mode_text , (width/4,height/4 + 65)) 
    screen.blit(quit_text , ((width/4) + 50,height/4 + 130)) 
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == pygame.MOUSEBUTTONDOWN:
            start_menu = False
            pygame.display.set_caption("Capture The Flag")
            running = True
    

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
    if i > 0:
        ai_tank = ai.Ai(tank, game_objects_list, tanks_list, space, current_map)
        ai_list.append(ai_tank)


#-- Create the flag
flag = gameobjects.Flag(current_map.flag_position[0], current_map.flag_position[1])
game_objects_list.append(flag)

#-- Create the bases
for i in range(0, len(current_map.start_positions)):
    position = current_map.start_positions[i]
    base = gameobjects.GameVisibleObject(position[0], position[1], images.bases[i])
    game_objects_list.append(base)

        
def tank_movement_handler(player_list):
    """Controls the movement and shooting for all tanks"""
    for player in player_list:

        if event.type == KEYDOWN:
            if event.key == player["Forward"]:
                tanks_list[player["Index"]].accelerate()

            if event.key == player["Reverse"]:
                tanks_list[player["Index"]].decelerate()

            if event.key == player["Turn_left"]:
                tanks_list[player["Index"]].turn_left()

            if event.key == player["Turn_right"]:
                tanks_list[player["Index"]].turn_right()

            tank = tanks_list[player["Index"]]

            if event.key == player["Shoot"] and \
                (pygame.time.get_ticks() >= tank.shot_delay):
                game_objects_list.append(tank.shoot(space))
                tank.shot_delay = pygame.time.get_ticks() + 1000 

        if event.type == KEYUP:
            if event.key == player["Forward"] or event.key == player["Reverse"]:
                tanks_list[player["Index"]].stop_moving()

            if event.key == player["Turn_left"] or event.key == player["Turn_right"]:
                tanks_list[player["Index"]].stop_turning()



def play_explosion_anim(bullet):
    game_objects_list.append(bullet.explosion(space))

    for obj in game_objects_list:
        if isinstance(obj, gameobjects.Explosion):
            if obj.stop:
                game_objects_list.remove(obj)


def collision_bullet_bullet(arb, space, data):
    """Handles collisions between tanks and bullets"""
    bullet1 = arb.shapes[0]
    bullet2 = arb.shapes[1]

    space.remove(bullet1, bullet1.body)
    game_objects_list.remove(bullet1.parent)

    space.remove(bullet2, bullet2.body)
    game_objects_list.remove(bullet2.parent)
    play_explosion_anim(bullet1.parent)
    return False


def collision_bullet_tank(arb, space, data):
    """Handles collisions between tanks and bullets"""
    bullet_shape = arb.shapes[0]
    tank = arb.shapes[1].parent

    if tank != bullet_shape.parent.tank:
        space.remove(bullet_shape, bullet_shape.body)
        game_objects_list.remove(bullet_shape.parent)
        gameobjects.Tank.respawn(tank)
        gameobjects.Tank.drop_flag(tank, flag)
        play_explosion_anim(bullet_shape.parent)

    return False


def collision_bullet_box(arb, space, data):
    """Handles collisions between bullets and boxes"""
    bullet_shape = arb.shapes[0]
    box = arb.shapes[1]
    space.remove(bullet_shape, bullet_shape.body)
    game_objects_list.remove(bullet_shape.parent)

    space.remove(box, box.body)
    game_objects_list.remove(box.parent)
    play_explosion_anim(bullet_shape.parent)
    return False


def ind_collision_bullet_box(arb, space, data):
    """Handels collisions between bullets and indestructable objects"""
    bullet_shape = arb.shapes[0]
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

#print(ai.Ai.find_shortest_path(ai_list[2]))




#-- Control whether the game run

while running:

    player1 = {"Index" : 0,\
           "Forward" : pygame.K_UP,\
           "Reverse": pygame.K_DOWN,\
           "Turn_left": pygame.K_LEFT,\
           "Turn_right": pygame.K_RIGHT,\
           "Shoot": pygame.K_SPACE,\
           "Time": 0}

    player2 = {"Index": 1,\
           "Forward": pygame.K_w,\
           "Reverse": pygame.K_s,\
           "Turn_left": pygame.K_a,\
           "Turn_right": pygame.K_d,\
           "Shoot": pygame.K_q,\
           "Time": 0}
    
    player_list = [player1]
    
    for tank_ai in ai_list:
        ai.Ai.decide(tank_ai)

    for tanks in tanks_list:
            gameobjects.Tank.try_grab_flag(tanks, flag)
            if tanks.has_won():
                running = False
    #-- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
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

