import pygame
from utils import get_asset_path
import utils

class Ground(pygame.sprite.Sprite):
    # Assets
    GROUND_IMG = pygame.transform.scale2x(pygame.image.load(get_asset_path("images", "environment", "ground.png")))

    # Movement
    VELOCITY = -4
    Y_POS = 710

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
