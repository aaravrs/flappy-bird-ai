import random

import pygame
from utils import get_asset_path
import utils

class Bird(pygame.sprite.Sprite):
    # Assets
    FRAME_1 = pygame.transform.scale2x(pygame.image.load(get_asset_path("images", "bird", "bird_frame_1.png")))
    FRAME_2 = pygame.transform.scale2x(pygame.image.load(get_asset_path("images", "bird", "bird_frame_2.png")))
    FRAME_3 = pygame.transform.scale2x(pygame.image.load(get_asset_path("images", "bird", "bird_frame_3.png")))

    # Spawn location
    BIRD_X = 230
    BIRD_Y = 350

    # Physics/Movement
    FLAP_STRENGTH = 14

    # Animation
    FLAP_TILT = 25
    NEGATIVE_TILT_EXPO = 1.24
    ANIMATION_SPEED = 0.33

    def __init__(self):
        super().__init__()

        self.x = Bird.BIRD_X
        self.y = Bird.BIRD_Y

        self.frames = [Bird.FRAME_1.convert_alpha(), Bird.FRAME_2.convert_alpha(), Bird.FRAME_3.convert_alpha(), Bird.FRAME_2.convert_alpha()] # Smooth animation
        self.animation_index = 0
        self.tilt = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.gravity = 0

        self.alive = True

    def get_player_input(self, events):
        for event in events:
            if self.alive:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Space bar
                    self.flap()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    self.flap()

    def flap(self): # TODO: Apply parabolic gravity
        self.gravity = -1 * Bird.FLAP_STRENGTH
        utils.audio_flap.play()

    def apply_gravity(self):
        self.rect.y += self.gravity
        self.gravity += 1

    def animate(self):
        if self.tilt >= -15: # Stops flapping when falling at a steep angle
            self.animation_index += Bird.ANIMATION_SPEED
            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)] # No need to remake rect, frames are same sizes
        else:
            self.image = self.frames[1]

        if self.gravity < 0: # Head tilt up while going upwards
            self.tilt = Bird.FLAP_TILT
        else: # Falling downwards, exponentially rotate
            # Tilt based on gravity
            self.tilt = -1 * self.gravity**(Bird.NEGATIVE_TILT_EXPO)
            if self.tilt < -90:
                self.tilt = -90

        self.image = pygame.transform.rotate(self.frames[int(self.animation_index)], self.tilt) # Do not repeatedly rotate same image
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self, events):
        if events == None: # Used for menu screen (static flapping animation)
            self.animate()
        else:
            self.get_player_input(events)
            if self.rect.bottom < random.randint(715, 730): # Stop moving the bird after hitting the ground
                self.apply_gravity()
            self.animate()
