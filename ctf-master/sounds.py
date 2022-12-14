import pygame
import os

pygame.mixer.init()

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_sound(file):
    """ Loads a soundfile fron data directory """
    file = os.path.join(main_dir, 'data', file)
    return pygame.mixer.Sound(file)

# def load_music(file):
#     """ Loads a soundfile fron data directory """
#     file = os.path.join(main_dir, 'data', file)
#     return pygame.mixer.music.load(file)


flag_sound = load_sound("flag_sound.wav")

shoot_sound = load_sound("tank_shoot_sound.wav")

box_sound = load_sound("box_sound.wav")

background_music = load_sound("background_music.wav")

tank_shot_sound = load_sound("tank_shot_sound.wav")

victory_sound = load_sound("victory_sound.wav")





