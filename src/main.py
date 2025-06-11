import random

import pygame
import neat
from sys import exit
import os
from pygame.examples.grid import WINDOW_HEIGHT

pygame.init()
# TODO: dpi scaling issue
# TODO convert alpha
# import ctypes
# try:
#     ctypes.windll.shcore.SetProcessDpiAwareness(1)  # PROCESS_SYSTEM_DPI_AWARE = 1
# except Exception:
#     try:
#         ctypes.windll.user32.SetProcessDPIAware()
#     except Exception:
#         pass

def get_asset_path(asset_name): # Platform neutral
    return os.path.join("../assets", asset_name)
#TODO: allow rescalablity
WIN_WIDTH = 500
WIN_HEIGHT = 800


class Bird(pygame.sprite.Sprite):
    FRAME_1 = pygame.transform.scale2x(pygame.image.load(get_asset_path("bird_frame_1.png")))
    FRAME_2 = pygame.transform.scale2x(pygame.image.load(get_asset_path("bird_frame_2.png")))
    FRAME_3 = pygame.transform.scale2x(pygame.image.load(get_asset_path("bird_frame_3.png")))
    FLAP_STRENGTH = 15
    FLAP_TILT = 25
    NEGATIVE_TILT_EXPO = 1.24
    ANIMATION_SPEED = 0.3

    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.frames = [Bird.FRAME_1.convert_alpha(), Bird.FRAME_2.convert_alpha(), Bird.FRAME_3.convert_alpha(), Bird.FRAME_2.convert_alpha()] # Smooth animation
        self.animation_index = 0
        self.tilt = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x, y))
        self.gravity = 0

    def get_player_input(self, events):
        # TODO sound
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.flap()

    def flap(self): # TODO: Apply parabolic gravity
        self.gravity = -1 * Bird.FLAP_STRENGTH
    def apply_gravity(self):
        self.rect.y += self.gravity
        self.gravity += 1
        # print(self.gravity)

    def animate(self):
        if self.tilt >= -15:
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
        self.get_player_input(events)
        self.apply_gravity()
        self.animate()
        # Animate

class Ground(pygame.sprite.Sprite):
    VELOCITY = -5
    Y_POS = 710
    GROUND_IMG = pygame.transform.scale2x(pygame.image.load(get_asset_path("ground.png")))

    def __init__(self, x):
        super().__init__()

        self.x = x
        self.y = Ground.Y_POS

        self.image = Ground.GROUND_IMG.convert()
        self.rect = self.image.get_rect(topleft = (self.x, self.y))


    def move(self):
        self.rect.x += Ground.VELOCITY

        if self.rect.right <= 0:
            self.rect.x += self.image.get_width() * 2 # Move it over the other image

    def update(self):
        self.move()

class Background(pygame.sprite.Sprite):
    BG_IMG = pygame.transform.scale2x(pygame.image.load(get_asset_path("background.png")))
    Y_POS = -100
    VELOCITY = -1
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.y = Background.Y_POS

        self.image = Background.BG_IMG.convert()
        self.rect = self.image.get_rect(topleft = (self.x, self.y))


    def move(self):
        self.rect.x += Background.VELOCITY

        if self.rect.right <= 0:
            self.rect.left += self.image.get_width() * 2
    def update(self):
        self.move()

class Pipe:
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load(get_asset_path("pipe.png")))
    VELOCITY = Ground.VELOCITY
    GAP = 200 # TODO change to account for bad movement
    def __init__(self, x):
        pass
        self.x = x
        self.height = 0
        self.top_y = 0
        self.bottom_y = 0
        self.set_heights()

        self.top_pipe = Pipe.TopPipe(self.x, self.top_y) # Coordinates of bottom left
        self.bottom_pipe = Pipe.BottomPipe(self.x, self.bottom_y)
        self.pipe_group = pygame.sprite.Group(
            self.top_pipe,
            self.bottom_pipe
        )

    def set_heights(self):
        # Testing found 50 - 450 to account for all valid ranges
        self.height = random.randint(50, 450)
        self.top_y = self.height
        self.bottom_y = self.height + Pipe.GAP


    def update(self):
        self.top_pipe.update()
        self.bottom_pipe.update()

    def draw(self, screen):
        self.pipe_group.draw(screen)


    class TopPipe(pygame.sprite.Sprite):

        def __init__(self, x, y):
            super().__init__()
            self.x = x
            self.y = y
            self.image = pygame.transform.flip(Pipe.PIPE_IMG.convert_alpha(), False, True)
            self.rect = self.image.get_rect(bottomleft = (self.x, self.y))

        def update(self):
            self.rect.x += Pipe.VELOCITY



    class BottomPipe(pygame.sprite.Sprite):

        def __init__(self, x, y):
            super().__init__()
            self.x = x
            self.y = y
            self.image = Pipe.PIPE_IMG.convert_alpha()
            self.rect = self.image.get_rect(topleft = (self.x, self.y))

        def update(self):
            self.rect.x += Pipe.VELOCITY

def main():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Bird(200, 200))
    bg_group = pygame.sprite.Group(
        Background(0),
        Background(Background.BG_IMG.get_width())
    )
    ground_group = pygame.sprite.Group(
    Ground(0),
        Ground(Ground.GROUND_IMG.get_width())
    )

    pipes = [Pipe(400), Pipe(800)]
    clock = pygame.time.Clock() # Will help limit framerate for consistency


    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #     player_group.sprite.gravity = -20


        bg_group.update()
        bg_group.draw(screen)

        player_group.update(events)
        player_group.draw(screen)


        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

        ground_group.update()
        ground_group.draw(screen)



        pygame.display.update()
        clock.tick(60) # Setting max framerate




if __name__ == "__main__":
    main()
