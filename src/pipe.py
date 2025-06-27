import pygame
from ground import Ground
import random
from bird import Bird
from utils import get_asset_path

class Pipe:
    # Assets
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load(get_asset_path("images", "environment", "pipe.png")))
    GAP = 200 # TODO change to account for bad movement

    # Movement
    VELOCITY = Ground.VELOCITY
    SPAWN_TIME = 1500 # ms

    def __init__(self, x):
        pass
        self.x = x
        self.height = 0
        self.top_y = 0
        self.bottom_y = 0
        self.set_heights()
        self.passed = False
        self.scored = False

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
        # Crossing center = passed
        if self.top_pipe.rect.centerx <= Bird.BIRD_X: self.passed = True

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
