import pygame
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    """ Load an image from the data directory. """
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert_alpha()

def load_animation(file,rows, columns, x, y):
    """ Load an animation sprite sheet from datat directory """
    image = load_image(file)
    image = pygame.transform.scale(image, (x, y))
    output=[]
    dx=(image.get_width()/columns)
    dy=(image.get_height()/rows)
    
    for row_index in range(rows):
        for column_index in range(columns):   
            pos=(dx*column_index, dy*row_index)
            output.append(image.subsurface(pos, (dx,dy) ) )

    return output

TILE_SIZE = 40 # Define the default size of tiles
 
explosion = load_image('explosion.png') # Image of an explosion

explosion_animation = load_animation('explosion_animation.png', 6, 8, 650, 500)
 
grass     = load_image('grass.png') # Image of a grass tile

rockbox   = load_image('rockbox.png') # Image of a rock box (wall)

metalbox  = load_image('metalbox.png') # Image of a metal box

woodbox   = load_image('woodbox.png') # Image of a wood box

flag      = load_image('flag.png') # Image of flag

bullet = load_image('bullet.png')
bullet = pygame.transform.scale(bullet, (10, 10))
bullet = pygame.transform.rotate(bullet, -90)

# List of image of tanks of different colors
tanks     = [load_image('tank_orange.png'), load_image('tank_blue.png'), load_image('tank_white.png'),
             load_image('tank_yellow.png'), load_image('tank_red.png'),  load_image('tank_gray.png')]

# List of image of bases corresponding to the color of each tank
bases     = [load_image('base_orange.png'), load_image('base_blue.png'), load_image('base_white.png'),
             load_image('base_yellow.png'), load_image('base_red.png'),  load_image('base_gray.png')]
