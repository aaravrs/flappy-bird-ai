import pygame
from pygame_widgets.slider import Slider
import pygame_widgets
import neat
from sys import exit # Platform neutral (not all interpreters have exit()/quit() by default)
import os
from enum import Enum

# Local imports
from background import Background
from bird import Bird
from ground import Ground
from pipe import Pipe
from utils import get_asset_path
import utils

# TODO: dpi scaling issue
# TODO: export game to exe
# TODO separate logic based on game activity
# TODO: allow rescalablity
# TODO: simply center x and center y of screen into variables for cleaner code
# TODO: make application logo
# screen.fill((0, 0, 0))  # TODO add to all menus (probably not needed since we blit over old frames)
# TODO: docstring (learn)

pygame.init()
utils.load_sounds()
utils.load_fonts()
show_fps = True

WIN_WIDTH = 500
WIN_HEIGHT = 800
MAX_FRAME_RATE = 60

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI")

# TODO: move to utils class
class Logo(pygame.sprite.Sprite):
    #TODO: make custom (animated) logo
    IMAGE = pygame.transform.scale_by(pygame.image.load(get_asset_path("images", "default_logo.png")), 0.18)

    def __init__(self):
        super().__init__()
        self.image = Logo.IMAGE.convert_alpha()
        self.rect = self.image.get_rect(center = (WIN_WIDTH // 2, 200))

    def update(self):
        self.image = self.image

# The global groups allows a seamless transition between the menu and the game
bg_group = pygame.sprite.Group(
    Background(0),
    Background(Background.BG_IMG.get_width())
)
ground_group = pygame.sprite.Group(
    Ground(0),
    Ground(Ground.GROUND_IMG.get_width())
)
logo_group = pygame.sprite.GroupSingle(
    Logo()
)
volume_slider = Slider(screen, 50, WIN_HEIGHT - 100,
                       400, 7,
                       min=0, max=100, initial=utils.VOLUME,
                       colour=(100, 100, 100), handleColour=(200, 200, 200), handleRadius=10)


class GameState(Enum):
    MENU = 0
    PLAYING_P = 1
    PLAYER_AI = 2
    SETTINGS = 3

class Button(pygame.sprite.Sprite):
    HOVER_OPACITY = 0.5
    BORDER_INFLATION_X = 50
    BORDER_INFLATION_Y = 10
    BORDER_RADIUS = 5

    def __init__(self, text, text_size, position, function):
        """Initalizes a button sprite""" #TODO: documentation



        super().__init__()
        self.DEFAULT_TEXT = utils.font_menu[text_size].render(text, False, (255, 255, 255))
        self.HOVER_TEXT = utils.font_menu[text_size].render(text, False, (155, 155, 155))

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

def test_func():
    print("Button pressed")

def display_stats(screen, score, fps, volume):
    def display_score(score):
        if score != None:
            score_surf = utils.font_fb[12].render(f"{score}", False, (255, 255, 255))
            score_rect = score_surf.get_rect(center=(WIN_WIDTH // 2, 100))
            score_surf_border = pygame.transform.scale_by(utils.font_fb[12].render(f"{score}", False, (0, 0, 0)), 1.1)
            screen.blit(score_surf_border, score_rect)  # Used to make an outline/shadow effect
            screen.blit(score_surf, score_rect)

    def display_fps(fps):
        fps_surf = utils.font_fb[5].render(f"{int(round(fps, 0))}", False, (255, 255, 255))
        fps_rect = fps_surf.get_rect(topright=(WIN_WIDTH - 10, 10))
        screen.blit(fps_surf, fps_rect)

    def display_volume(volume):
        if volume != None:
            volume_text = utils.font_menu[12].render(f"{utils.VOLUME}", False, (50, 50, 200))
            volume_rect = volume_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
            screen.blit(volume_text, volume_rect)

    display_score(score)
    display_fps(fps)
    display_volume(volume)


def menu_main():
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Bird())

    clock = pygame.time.Clock() # Used to set maximum framerate

    play_button = Button("Play", 12, (WIN_WIDTH // 2, WIN_HEIGHT // 2 ), menu_play)
    customize_button = Button("COMING SOON", 10, (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100), menu_play)
    exit_button = Button("Exit", 7, (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 200), exit)

    button_group = pygame.sprite.Group(
        play_button,
        customize_button,
        exit_button
    )

    while True:
        fps = clock.get_fps()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        bg_group.update()
        bg_group.draw(screen)

        player_group.update(None)
        player_group.draw(screen)

        ground_group.update()
        ground_group.draw(screen)

        button_group.update(screen, events)
        button_group.draw(screen)

        logo_group.update()
        logo_group.draw(screen)

        utils.VOLUME = volume_slider.getValue()
        utils.update_volume()


        display_stats(screen, None, fps, utils.VOLUME)
        pygame_widgets.update(events)
        pygame.display.update()
        clock.tick(MAX_FRAME_RATE) # Setting max framerate

def menu_play():
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Bird())

    clock = pygame.time.Clock() # Used to set maximum framerate

    human_button = Button("Human", 12, (WIN_WIDTH // 2, WIN_HEIGHT // 2), game_player)
    ai_button = Button("AI (Neural Network)", 12, (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100), game_ai)
    back_button = Button("Back", 7, (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 200), menu_main)

    button_group = pygame.sprite.Group(
        human_button,
        ai_button,
        back_button
    )

    while True:
        fps = clock.get_fps()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        bg_group.update()
        bg_group.draw(screen)

        player_group.update(None)
        player_group.draw(screen)

        ground_group.update()
        ground_group.draw(screen)

        button_group.update(screen, events)
        button_group.draw(screen)

        logo_group.update()
        logo_group.draw(screen)

        utils.VOLUME = volume_slider.getValue()
        utils.update_volume()

        pygame_widgets.update(events)
        display_stats(screen, None, fps, utils.VOLUME)
        pygame.display.update()
        clock.tick(MAX_FRAME_RATE) # Setting max framerate

def game_player():
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Bird())
    bird = player_group.sprite # Reference/pointer to player bird

    score = 0
    pipes = []

    # Timer to spawn pipes
    pipe_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(pipe_timer, Pipe.SPAWN_TIME)

    clock = pygame.time.Clock() # Used to set maximum framerate

    while True:
        fps = clock.get_fps()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pipe_timer:
                pipes.append(Pipe(WIN_WIDTH))


        if bird.alive: bg_group.update()
        bg_group.draw(screen)

        player_group.update(events)
        player_group.draw(screen)

        pipes_to_remove = []



        # TODO: add death to ground & pipe
        for pipe in pipes:
            if (bird.alive and
                    (pygame.sprite.collide_mask(player_group.sprite, pipe.top_pipe) or
                     pygame.sprite.collide_mask(player_group.sprite, pipe.bottom_pipe))): # TODO: optimize, new mask each time
                player_group.sprite.alive = False
                utils.audio_hit.play()
                utils.audio_die.play()

        for ground_sprite in ground_group.sprites():
            if bird.alive and pygame.sprite.collide_mask(player_group.sprite, ground_sprite): # TODO: optimize, new mask each time
                player_group.sprite.alive = False
                utils.audio_hit.play()


        for pipe in pipes:
            # pygame.draw.line(screen, (255, 0, 0), bird.rect.center,
            #                  pipe.top_pipe.rect.midbottom)
            # pygame.draw.line(screen, (255, 0, 0), bird.rect.center,
            #                  pipe.bottom_pipe.rect.midtop)

            if bird.alive: pipe.update()

            if  pipe.top_pipe.rect.right < 0:
                pipes_to_remove.append(pipe) # Remove pipe when out of screen

            if pipe.passed and not pipe.scored: # Only score once per pipe
                score += 1
                pipe.scored = True
                utils.audio_point.play()

            pipe.draw(screen)



        if bird.alive: ground_group.update()
        ground_group.draw(screen)

        for pipe_to_remove in pipes_to_remove: # Removing off-screen pipes
            pipes.remove(pipe_to_remove)

        display_stats(screen, score, fps, None)
        pygame.display.update()
        clock.tick(MAX_FRAME_RATE) # Setting max framerate

def game_ai():
    # TODO: mute volume until a certain threshold of birds left
    pass

#TODO: Finite state machine to manage scenes (menu, game, ai game)
def main():
    # utils.audio_die.play(loops = -1)
    menu_main()

if __name__ == "__main__":
    main()
