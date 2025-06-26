import os
import pygame

# CONFIG FOR GAME MECHANICS
#TODO: add vars for each mechanics (flap strength, speed, etc)

FONT_SIZES = (4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52) # Max index = 12; Size = (Index + 1) * 4

def get_asset_path(type, asset_name): # Platform neutral
    return os.path.join("../assets", type, asset_name) # TODO check if this works with back slash

# Can only be called after pygame.init() in main.py
def load_sounds():
    global audio_point, audio_flap, audio_hit, audio_die

    audio_point = pygame.mixer.Sound(get_asset_path("audio", "point.wav"))
    audio_point.set_volume(0.2)

    audio_flap = pygame.mixer.Sound(get_asset_path("audio", "wing.wav"))
    audio_flap.set_volume(0.2)

    audio_hit = pygame.mixer.Sound(get_asset_path("audio", "hit.wav"))
    audio_hit.set_volume(0.2)

    audio_die = pygame.mixer.Sound(get_asset_path("audio", "die.wav"))
    audio_die.set_volume(0.2)

def load_fonts():
    global font_fb, font_menu

    font_fb = []
    font_menu = []
    for size in FONT_SIZES:
        font_fb.append(pygame.font.Font(get_asset_path("fonts", "04B_19.TTF"), size))
        font_menu.append(pygame.font.Font(get_asset_path("fonts", "ThaleahFat.ttf"), size))



#TODO pixel perfect collision
# https://stackoverflow.com/questions/48025283/pixel-perfect-collision-detection-for-sprites-with-a-transparent-background