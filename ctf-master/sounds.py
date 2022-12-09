import pygame
import os

pygame.mixer.init()

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_sound(file):
    file = os.path.join(main_dir, 'data', file)

    return pygame.mixer.Sound(file)

flag_sound = load_sound("flag_sound.wav")

shoot_sound = load_sound("tank_shoot_sound.wav")

box_sound = load_sound("box_sound.wav")

background_music = load_sound("background_music.wav")

tank_shot_sound = load_sound("tank_shot_sound.wav")

# flag_sound = pygame.mixer.Sound("data/flag_sound.wav")

# shoot_sound = pygame.mixer.Sound("data/tank_shoot_sound.wav")

# box_sound = pygame.mixer.Sound("data/box_sound.wav")

# background_music = pygame.mixer.Sound("data/background_music.wav")

# tank_shot_sound = pygame.mixer.Sound("data/tank_shot_sound.wav")




