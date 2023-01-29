import gameobjects
import images
import pymunk
import pygame


#-- Functions for generating the background,
#-- and the elements it should contain


#-- Create the boxes
def create_boxes(current_map, game_objects_list, space):
    """Create boxes according to map layout"""
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # Get the type of boxes
            box_type  = current_map.boxAt(x, y)
            # If the box type is not 0 (aka grass tile), create a box
            if(box_type != 0):
                # Create a "Box" using the box_type, 
                # aswell as the x,y coordinates,
                # and the pymunk space
                box = gameobjects.get_box_with_type(x, y, box_type, space)
                game_objects_list.append(box)


#-- Create the flag
def create_flag(current_map, game_objects_list):
    """Create flag object"""
    flag = gameobjects.Flag(current_map.flag_position[0],
     current_map.flag_position[1])
    game_objects_list.append(flag)
    return flag


#-- Create the bases
def create_bases(current_map, game_objects_list):
    """Creates the bases where each tank spawns"""
    for i in range(0, len(current_map.start_positions)):
        position = current_map.start_positions[i]
        base = gameobjects.GameVisibleObject(
            position[0], position[1], images.bases[i])
        game_objects_list.append(base)


#Creates barriers
def create_barriers(current_map, space):
    """Creates barriers that limit the map"""
    static_body = space.static_body
    barrier_list = [pymunk.Segment(static_body, (0, 0),
        (0, current_map.height), 0.0), 
    
    pymunk.Segment(static_body, (0, current_map.height),
        (current_map.width, current_map.height), 0.0),
    
    pymunk.Segment(static_body, (current_map.width, current_map.height), 
        (current_map.width, 0), 0.0),
    
    pymunk.Segment(static_body, (current_map.width, 0), (0, 0), 0.0)
    ]

    space.add(*barrier_list)


def create_background(current_map, screen):
    """Create game background"""
    background = pygame.Surface(screen.get_size())

    #   Copy the grass tile all over the level area
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # The call to the function "blit" will copy the image
            # contained in "images.grass" into the "background"
            # image at the coordinates given as the second argument
            background.blit(images.grass,
              (x*images.TILE_SIZE, y*images.TILE_SIZE))
    return background


def create_enviroment(current_map, game_objects_list, space):
    """Creates barries, boxes and bases"""
    create_barriers(current_map, space)
    create_bases(current_map, game_objects_list)
    create_boxes(current_map, game_objects_list, space)