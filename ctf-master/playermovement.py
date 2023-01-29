import gameobjects
import pygame
from pygame.locals import *


#-- Player controls and tank movemment


def add_players(tanks_list, singleplayer, multiplayer):
    """Adds human players to the game according to game mode"""
    #-- Player dictionaries
    player1 = {"Index": 0,
            pygame.K_UP: tanks_list[0].accelerate,
            pygame.K_DOWN: tanks_list[0].decelerate,
            pygame.K_LEFT: tanks_list[0].turn_left,
            pygame.K_RIGHT: tanks_list[0].turn_right,
            pygame.K_SPACE: tanks_list[0].shoot
            }


    player2 = {"Index": 1,
            pygame.K_w: tanks_list[1].accelerate,
            pygame.K_s: tanks_list[1].decelerate,
            pygame.K_a: tanks_list[1].turn_left,
            pygame.K_d: tanks_list[1].turn_right,
            pygame.K_q: tanks_list[1].shoot
            }

    # Add human players
    if singleplayer:
        player_list = [player1] 
    if multiplayer:
        player_list = [player1, player2]
    
    return player_list


def tank_movement_handler(player_list, game_objects_list, tanks_list,
                        event, space):
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