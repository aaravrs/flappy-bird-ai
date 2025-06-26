import os
import pygame

from enum import Enum

class Font(Enum):
    FB = 1
    MENU = 2


DEFAULT_VOLUME = 50
VOLUME = DEFAULT_VOLUME
# CONFIG FOR GAME MECHANICS
#TODO: add vars for each mechanic (flap strength, speed, etc)

FONT_SIZES = (4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68) # Max index = 16; Size = (Index + 1) * 4

def get_asset_path(type, asset_name): # Platform neutral
    return os.path.join("../assets", type, asset_name) # TODO check if this works with back slash

def get_shadow_font(size, text, font, AA, color, shadow_color, coordinates):
    shadow_distance = 5

    # {
    #     "base": {"surf": ..., "rect": ...}
    #     "shadow": {"surf": ..., "rect": ...}
    # }
    font_using = None
    ret = {}

    if font == Font.FB:
        font_using = font_fb
    elif font == Font.MENU:
        font_using = font_menu
    else:
        return None

    base_text = font_using[size].render(text, AA, color)
    base_text_rect = base_text.get_rect(center = coordinates)
    ret["base"] = {"surf": base_text, "rect": base_text_rect}

    shadow_text = font_using[size].render(text, AA, shadow_color)
    shadow_text_rect = shadow_text.get_rect(center = (coordinates[0] + shadow_distance, coordinates[1] + shadow_distance))
    ret["shadow"] = {"surf": shadow_text, "rect": shadow_text_rect}


    return ret




    # Can only be called after pygame.init() in main.py
def load_sounds():
    global audio_point, audio_flap, audio_hit, audio_die

    audio_point = pygame.mixer.Sound(get_asset_path("audio", "point.wav"))
    audio_flap = pygame.mixer.Sound(get_asset_path("audio", "wing.wav"))
    audio_hit = pygame.mixer.Sound(get_asset_path("audio", "hit.wav"))
    audio_die = pygame.mixer.Sound(get_asset_path("audio", "die.wav"))
    update_volume()

# Can only be called after initializing sounds
def update_volume():
    # TODO: base volume off of factor x original volume
    audio_point.set_volume(0.2 * (VOLUME / 100))
    audio_flap.set_volume(0.4 * (VOLUME / 100))
    audio_hit.set_volume(0.3 * (VOLUME / 100))
    audio_die.set_volume(0.4 * (VOLUME / 100))


def load_fonts():
    global font_fb, font_menu

    font_fb = []
    font_menu = []
    for size in FONT_SIZES:
        font_fb.append(pygame.font.Font(get_asset_path("fonts", "04B_19.TTF"), size))
        font_menu.append(pygame.font.Font(get_asset_path("fonts", "Ithaca.ttf"), size))



#TODO pixel perfect collision
# https://stackoverflow.com/questions/48025283/pixel-perfect-collision-detection-for-sprites-with-a-transparent-background