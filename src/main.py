import pygame
import neat
from sys import exit
import os
from pygame.examples.grid import WINDOW_HEIGHT

pygame.init()
# TODO: dpi scaling issue
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
BG_IMG = pygame.transform.scale2x(pygame.image.load(get_asset_path("background.png")))
GROUND_IMG = pygame.transform.scale2x(pygame.image.load(get_asset_path("ground.png")))
#TODO: allow rescalablity
WIN_WIDTH = 500
WIN_HEIGHT = 800


class Bird(pygame.sprite.Sprite):
    FRAME_1 = pygame.transform.scale2x(pygame.image.load(get_asset_path("bird_frame_1.png")))
    FRAME_2 = pygame.transform.scale2x(pygame.image.load(get_asset_path("bird_frame_2.png")))
    FRAME_3 = pygame.transform.scale2x(pygame.image.load(get_asset_path("bird_frame_3.png")))

    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.frames = [Bird.FRAME_1, Bird.FRAME_2, Bird.FRAME_3]
        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x, y))
        self.gravity = 0

    def get_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print("Flap")
            # TODO sounds
            self.gravity = -20

    def apply_gravity(self):
        self.rect.y += self.gravity
        self.gravity += 1

    def update(self):
        self.get_player_input()
        self.apply_gravity()
        # Animate







def main():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Bird(200, 200))
    clock = pygame.time.Clock() # Will help limit framerate for consistency

    # Timer

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()



        screen.blit(BG_IMG, (0, -100))
        screen.blit(GROUND_IMG, (0, 710))

        player_group.update()
        player_group.draw(screen)

        pygame.display.update()
        clock.tick(60) # Setting max framerate




if __name__ == "__main__":
    main()
