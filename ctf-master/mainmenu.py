import os
import sys
import pygame
from pygame.locals import *
from pygame.color import *
import button
import maps


# --- Menu flag variables
menu = True
start_menu = True
settings_menu = False
game_mode_menu = False
map_menu = False

# --- Game variables
current_map = maps.map0
current_mode = "Singleplayer"
current_map_string = "Map 1"
singleplayer = True
multiplayer = False

# --- Creates the screen and offset
menu_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.Surface(current_map.rect().size)
screen_offset = tuple([(x[0]-x[1])/2 for x in zip( menu_screen.get_size(), screen.get_size() )])


# --- Creating and rendering fonts and colours
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

start_menu_buttons = [play_button, settings_button, quit_button]

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

settings_menu_buttons = [game_mode_button, map_button, back_button]

#--GameMode menu buttons
single_player_button = button.Button(400, 100, width/3, height/4, 
                                     button_colour, b_hover_colour, 
                                     "Singleplayer", font, white)

hot_seat_mult_button = button.Button(400, 100, width*2/3, height/4, 
                                     button_colour, b_hover_colour, 
                                     "Multiplayer", font, white)

game_mode_menu_buttons = [single_player_button, hot_seat_mult_button, back_button]

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

map_menu_buttons = [map1_button, map2_button, map3_button, back_button]



def show_start_menu():
    """Lets the player start the game, quit or go to game settings"""
    global menu
    global running
    global start_menu
    global settings_menu

    pygame.display.set_caption("Main menu")
    menu_screen.fill(menu_colour)

    for elem in start_menu_buttons:
        elem.draw(menu_screen)

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
    


def show_settings_menu():
    """Main menu for selecting which settings to change"""
    global settings_menu
    global game_mode_menu
    global map_menu
    global start_menu

    pygame.display.set_caption("Settings")
    menu_screen.fill(menu_colour)

    for elem in settings_menu_buttons:
        elem.draw(menu_screen)

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

    
def show_game_mode_menu():
    """Lets the player choose game mode"""
    global singleplayer
    global multiplayer
    global current_mode
    global game_mode_menu
    global settings_menu

    pygame.display.set_caption("Game-mode menu")
    menu_screen.fill(menu_colour)

    for elem in game_mode_menu_buttons:
        elem.draw(menu_screen)

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


def show_map_menu():
    """Lets the player choose which map to play in"""
    global settings_menu
    global map_menu
    global current_map
    global current_map_string
    global screen
    global menu_screen
    global menu_colour

    pygame.display.set_caption("Map Selection")
    menu_screen.fill(menu_colour)

    for elem in map_menu_buttons:
        elem.draw(menu_screen)

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


def show_menu(main_clock, framerate):
    """Handles which sub menu that should be shown"""
    while menu:
    # Creates the start menu and handles its events
        if start_menu:
            show_start_menu()
            
        # Creates the settings menu and handles its events
        if settings_menu:
            show_settings_menu()

        #Creates the game_mode_menu and handles its events
        if game_mode_menu:
            show_game_mode_menu()

        # Creates the map menu and handles its events
        if map_menu:
            show_map_menu()

        pygame.display.update()    
        main_clock.tick(framerate)


def get_game_mode():
    """Returns the game mode chosen in the game mode menu"""
    return singleplayer, multiplayer


def get_screen():
    """Returns screen variables"""
    return screen, menu_screen, screen_offset


def get_map():
    """Returns current game map"""
    return current_map
