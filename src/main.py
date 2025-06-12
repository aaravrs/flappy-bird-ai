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

pygame.init()
show_fps = True
# TODO: dpi scaling issue
# TODO separate logic based on game activity
# TODO: allow rescalablity

WIN_WIDTH = 500
WIN_HEIGHT = 800
MAX_FRAME_RATE = 60

font_fb = []
for size in utils.FONT_SIZES:
    font_fb.append(pygame.font.Font(get_asset_path("fonts", "04B_19.TTF"), size))


class GameState(Enum):
    MENU = 0
    PLAYING_P = 1
    PLAYER_AI = 2
    SETTINGS = 3
def display_stats(screen, score, fps):
    score_surf = font_fb[12].render(f"{score}", False, (255, 255, 255))
    score_rect = score_surf.get_rect(center = (WIN_WIDTH / 2, 100))
    screen.blit(score_surf, score_rect)
    if show_fps:
        fps_surf = font_fb[5].render(f"{int(round(fps, 0))}", False, (255, 255, 255))
        fps_rect = score_surf.get_rect(topright = (WIN_WIDTH - 10, 10)) # TODO fix glitch
        screen.blit(fps_surf, fps_rect)


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
            if  pipe.top_pipe.rect.left + Pipe.PIPE_IMG.get_width() < 0:
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

        pygame.display.update()
        clock.tick(MAX_FRAME_RATE) # Setting max framerate

if __name__ == "__main__":
    main()
