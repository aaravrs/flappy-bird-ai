import pygame
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
# TODO separate logic based on game activity
# TODO: allow rescalablity

pygame.init()
utils.load_sounds()
utils.load_fonts()
show_fps = True

WIN_WIDTH = 500
WIN_HEIGHT = 800
MAX_FRAME_RATE = 60

class GameState(Enum):
    MENU = 0
    PLAYING_P = 1
    PLAYER_AI = 2
    SETTINGS = 3


class Button(pygame.sprite.Sprite):
    HOVER_OPACITY = 0.5
    BORDER_INFLATION_X = 50
    BORDER_INFLATION_Y = 10
    BORDER_RADIUS = 50

    def __init__(self, text, text_size, position, function):
        """Initalizes a button sprite""" #TODO: documentation



        super().__init__()
        self.DEFAULT_TEXT = utils.font_menu[text_size].render(text, False, (255, 255, 255))
        self.HOVER_TEXT = utils.font_menu[text_size].render(text, False, (155, 155, 155))

        self.image = self.DEFAULT_TEXT
        self.rect = self.image.get_rect(center = position)

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



def display_stats(screen, score, fps):
    score_surf = utils.font_fb[12].render(f"{score}", False, (255, 255, 255))
    score_rect = score_surf.get_rect(center = (WIN_WIDTH / 2, 100))
    screen.blit(score_surf, score_rect)
    if show_fps:
        fps_surf = utils.font_fb[5].render(f"{int(round(fps, 0))}", False, (255, 255, 255))
        fps_rect = score_surf.get_rect(topright = (WIN_WIDTH - 10, 10)) # TODO fix glitch
        screen.blit(fps_surf, fps_rect)



def main_menu():
    pass




#TODO: Finite state machine to manage scenes (menu, game, ai game)
def main():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird - Player")
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Bird())
    pygame.display.set_icon(player_group.sprite.frames[1]) # TODO: change icon based on mode
    bg_group = pygame.sprite.Group(
        Background(0),
        Background(Background.BG_IMG.get_width())
    )
    ground_group = pygame.sprite.Group(
    Ground(0),
        Ground(Ground.GROUND_IMG.get_width())
    )

    score = 0
    pipes = []

    # Timer to spawn pipes
    pipe_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(pipe_timer, Pipe.SPAWN_TIME)

    clock = pygame.time.Clock() # Used to set maximum framerate


    #TODO: testing
    play_button = Button("Play", 12, (WIN_WIDTH // 2, WIN_HEIGHT / 2), test_func)
    exit_button = Button("Exit", 10, (WIN_WIDTH // 2, WIN_HEIGHT / 2 + 100), exit)

    button_group = pygame.sprite.Group(
        play_button,
        exit_button
    )
    human_option_button = Button("Play", 12, (WIN_WIDTH // 2, WIN_HEIGHT / 2), test_func)
    ai_option_button = Button("Play", 12, (WIN_WIDTH // 2, WIN_HEIGHT / 2), test_func)

    while True:
        fps = clock.get_fps()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pipe_timer:
                pipes.append(Pipe(WIN_WIDTH))


        bg_group.update()
        bg_group.draw(screen)

        player_group.update(events)
        player_group.draw(screen)

        pipes_to_remove = []

        for pipe in pipes:
            pipe.update()

            #TODO fix order (update, statements, then draw)
            if  pipe.top_pipe.rect.right < 0:
                print("Deleted")
                pipes_to_remove.append(pipe)
            if pipe.passed and not pipe.scored: # Only score once per pipe
                score += 1
                pipe.scored = True

            pipe.draw(screen)

        ground_group.update()
        ground_group.draw(screen)

        display_stats(screen, score, fps)
        for pipe_to_remove in pipes_to_remove:
            pipes.remove(pipe_to_remove)

        #TODO: testing
        button_group.update(screen, events)
        button_group.draw(screen)


        pygame.display.update()
        clock.tick(MAX_FRAME_RATE) # Setting max framerate


    while True: # Main menu
        pass


if __name__ == "__main__":
    main()
