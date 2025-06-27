import os
import pygame

from enum import Enum


# === Game Configuration === #
WIN_WIDTH = 500 # TODO: make game compatible with any width
WIN_HEIGHT = 800

WIN_CENTER_X = WIN_WIDTH // 2
WIN_CENTER_Y = WIN_HEIGHT // 2

MAX_FRAME_RATE = 60

#TODO: add vars for each mechanic (flap strength, speed, etc) (to allow playground for ai gamemode)

# # # # # # # # # # # # # # # HELPER # # # # # # # # # # # # # # #

# === Game Configuration === #
def get_asset_path(*parts): # Platform neutral
    return os.path.join("..", "assets", *parts)

class Button(pygame.sprite.Sprite):
    HOVER_OPACITY = 0.5
    BORDER_INFLATION_X = 50
    BORDER_INFLATION_Y = 10
    BORDER_RADIUS = 5

    def __init__(self, text, text_size, position, function):
        """Initalizes a button sprite""" #TODO: documentation

        super().__init__()
        self.DEFAULT_TEXT = font_menu[text_size].render(text, False, (255, 255, 255))
        self.HOVER_TEXT = font_menu[text_size].render(text, False, (155, 155, 155))

        self.image = self.DEFAULT_TEXT
        self.rect = self.image.get_rect(midtop = position)

        self.function = function
        pass


    def update(self, screen, events):
        # Draw the border rectangle before the group.draw method is called

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (100, 100, 100), self.rect.inflate(Button.BORDER_INFLATION_X, Button.BORDER_INFLATION_Y), border_radius = Button.BORDER_RADIUS)
            self.image = self.HOVER_TEXT

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.function()

        else:
            pygame.draw.rect(screen, (0, 0, 0), self.rect.inflate(Button.BORDER_INFLATION_X, Button.BORDER_INFLATION_Y), border_radius = Button.BORDER_RADIUS)
            self.image = self.DEFAULT_TEXT

class Logo(pygame.sprite.Sprite):
    #TODO: make custom (animated) logo
    IMAGE = pygame.transform.scale_by(pygame.image.load(get_asset_path("images", "menu", "default_logo.png")), 0.18)

    def __init__(self):
        super().__init__()
        self.image = Logo.IMAGE.convert_alpha()
        self.rect = self.image.get_rect(center = (WIN_CENTER_X, 200))

    def update(self):
        self.image = self.image


# # # # # # # # # # # # # # # TEXT # # # # # # # # # # # # # # #

# Max index = 16; Size = (Index + 1) * 4
FONT_SIZES = (4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68)
class Font(Enum):
    FB = 1
    MENU = 2

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

def load_fonts():
    global font_fb, font_menu

    font_fb = []
    font_menu = []
    for size in FONT_SIZES:
        font_fb.append(pygame.font.Font(get_asset_path("fonts", "04B_19.TTF"), size))
        font_menu.append(pygame.font.Font(get_asset_path("fonts", "Ithaca.ttf"), size))

# # # # # # # # # # # # # # # SOUNDS # # # # # # # # # # # # # # #

DEFAULT_VOLUME = 50
VOLUME = DEFAULT_VOLUME

def load_sounds():
    global audio_point, audio_flap, audio_hit, audio_die

    audio_point = pygame.mixer.Sound(get_asset_path("audio", "sfx", "point.wav"))
    audio_flap = pygame.mixer.Sound(get_asset_path("audio", "sfx", "wing.wav"))
    audio_hit = pygame.mixer.Sound(get_asset_path("audio", "sfx", "hit.wav"))
    audio_die = pygame.mixer.Sound(get_asset_path("audio", "sfx", "die.wav"))
    update_volume()

# Can only be called after initializing sounds
def update_volume():
    # TODO: base volume off of factor x original volume
    audio_point.set_volume(0.2 * (VOLUME / 100))
    audio_flap.set_volume(0.4 * (VOLUME / 100))
    audio_hit.set_volume(0.3 * (VOLUME / 100))
    audio_die.set_volume(0.4 * (VOLUME / 100))


