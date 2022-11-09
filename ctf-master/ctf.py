import pygame
from pygame.locals import *
from pygame.color import *
import pymunk

#----- Initialisation -----#

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

#-- Constants
FRAMERATE = 50

#-- Variables
#   Define the current level
current_map         = maps.map0
#   List of all game objects
game_objects_list   = []
tanks_list          = []


#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)


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




#-- Create the flag
flag = gameobjects.Flag(current_map.flag_position[0], current_map.flag_position[1])
game_objects_list.append(flag)

#Create bases
for i in range(0, len(current_map.start_positions)):
    position = current_map.start_positions[i]
    base = gameobjects.GameVisibleObject(position[0], position[1], images.bases[i])
    game_objects_list.append(base)


def collision_bullet_tank(arb, space, data):
    bullet_shape = arb.shapes[0]
    tank = arb.shapes[1].parent
    # print(bullet_shape.parent.tank)
    # print(tank)
    if tank != bullet_shape.parent.tank:
        space.remove(bullet_shape, bullet_shape.body)
        game_objects_list.remove(bullet_shape.parent)
        gameobjects.Tank.respawn(tank)
    return False
handler = space.add_collision_handler(1, 2)
handler.pre_solve = collision_bullet_tank



def collision_bullet_box(arb, space, data):
    bullet_shape = arb.shapes[0]
    box = arb.shapes[1]

    space.remove(bullet_shape, bullet_shape.body)
    game_objects_list.remove(bullet_shape.parent)

    space.remove(box, box.body)
    game_objects_list.remove(box.parent)
    return False

box_handler = space.add_collision_handler(1, 3)
box_handler.pre_solve = collision_bullet_box

def ind_collision_bullet_box(arb, space, data):
    bullet_shape = arb.shapes[0]
    space.remove(bullet_shape, bullet_shape.body)
    game_objects_list.remove(bullet_shape.parent)
    return False
indestructible_handler = space.add_collision_handler(1, 0)
indestructible_handler.pre_solve = ind_collision_bullet_box



#----- Main Loop -----#

#-- Control whether the game run
running = True

skip_update = 0

while running:
    #-- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        for tanks in tanks_list:
            gameobjects.Tank.try_grab_flag(tanks, flag)
        
        if tanks_list[0].has_won():
            running = False
        
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                tanks_list[0].accelerate()

            elif event.key == K_DOWN:
                tanks_list[0].decelerate()

            elif event.key == K_RIGHT:
                tanks_list[0].turn_right()

            elif event.key == K_LEFT:
                tanks_list[0].turn_left()
            
            elif event.key == K_SPACE:
                bullet = tanks_list[0].shoot(space)#gameobjects.Tank.shoot(tanks_list[0], space)
                game_objects_list.append(bullet)

                
            


        elif event.type == KEYUP:
            if event.key == K_UP:
                tanks_list[0].stop_moving()

            elif event.key == K_DOWN:
                tanks_list[0].stop_moving()

            elif event.key == K_RIGHT:
                tanks_list[0].stop_turning()

            elif event.key == K_LEFT:
                tanks_list[0].stop_turning()

             
        
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
