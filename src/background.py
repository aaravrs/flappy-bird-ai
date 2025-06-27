import pygame
from utils import get_asset_path
import utils

class Background(pygame.sprite.Sprite):
    # Assets
    BG_IMG = pygame.transform.scale2x(pygame.image.load(get_asset_path("images", "environment", "background.png")))

    # Movement
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
