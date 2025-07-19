# # # # # # # # # # # # # # # MAIN MENU # # # # # # # # # # # # # # #

# Standard library
from sys import exit # Platform neutral (not all interpreters have exit()/quit() by default)

# Third-party
import pygame
from pygame_widgets.slider import Slider
import pygame_widgets
import neat

# Local
from background import Background
from bird import Bird
from ground import Ground
from pipe import Pipe
from utils import (
    get_asset_path,
    Button,
    ToggleButton,
    Logo,
    WIN_WIDTH,
    WIN_HEIGHT,
    WIN_CENTER_X,
    WIN_CENTER_Y,
    MAX_FRAME_RATE,
)
import utils

# TODO: dpi scaling issue
# TODO: organize assets into grouped folders
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

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI")

#TODO: organize into "init_menu" function

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
volume_slider = Slider(screen, WIN_WIDTH // 2 - (400 / 2), WIN_HEIGHT - 100,
                       400, 7,
                       min=0, max=100, initial=utils.VOLUME,
                       colour=(100, 100, 100), handleColour=(200, 200, 200), handleRadius=10)



def display_stats(score, fps, volume):
    def display_score(score):
        if score != None:
            score_shadow = utils.get_shadow_font(14, f"{score}", utils.Font.FB,
                                                 False, (255, 255, 255), (0, 0, 0),
                                                 (WIN_CENTER_X, 100))

            screen.blit(score_shadow["shadow"]["surf"], score_shadow["shadow"]["rect"])
            screen.blit(score_shadow["base"]["surf"], score_shadow["base"]["rect"])

    def display_fps(fps):
        fps_surf = utils.font_fb[5].render(f"{int(round(fps, 0))}", False, (255, 255, 255))
        fps_rect = fps_surf.get_rect(topright=(WIN_WIDTH - 10, 10))
        screen.blit(fps_surf, fps_rect)

    def display_volume(volume):
        if volume != None:
            volume_text = utils.font_menu[12].render(f"{utils.VOLUME}", False, (50, 50, 200))
            volume_rect = volume_text.get_rect(center=(WIN_CENTER_X, WIN_HEIGHT - 50))
            screen.blit(volume_text, volume_rect)

    display_score(score)
    display_fps(fps)
    display_volume(volume)

# # # # # # # # # # # # # # # MAIN MENU # # # # # # # # # # # # # # #
def menu_main():
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Bird())

    clock = pygame.time.Clock() # Used to set maximum framerate

    play_button = Button("Play", 12, (WIN_CENTER_X, WIN_CENTER_Y), menu_play)
    customize_button = Button("COMING SOON", 10, (WIN_CENTER_X, WIN_CENTER_Y + 100), menu_play)
    exit_button = Button("Exit", 7, (WIN_CENTER_X, WIN_CENTER_Y + 200), exit, get_asset_path("images", "bird", "bird_frame_1.png"))
    # settings_button = Button("Settings", 7, (WIN_CENTER_X, WIN_CENTER_Y + 200), exit, get_asset_path("images", "bird", "bird_frame_1.png"))

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


        display_stats(None, fps, utils.VOLUME)
        pygame_widgets.update(events)
        pygame.display.update()
        clock.tick(MAX_FRAME_RATE) # Setting max framerate

# # # # # # # # # # # # # # # PLAY MENU # # # # # # # # # # # # # # #
def menu_play():
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Bird())

    clock = pygame.time.Clock() # Used to set maximum framerate

    human_button = Button("Human", 12, (WIN_CENTER_X, WIN_CENTER_Y), game_player)
    ai_button = Button("AI (Neural Network)", 12, (WIN_CENTER_X, WIN_CENTER_Y + 100), game_ai)
    back_button = Button("Back", 7, (WIN_CENTER_X, WIN_CENTER_Y + 200), menu_main)

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
        display_stats(None, fps, utils.VOLUME)
        pygame.display.update()
        clock.tick(MAX_FRAME_RATE) # Setting max framerate

# # # # # # # # # # # # # # # PLAYER GAME # # # # # # # # # # # # # # #
def game_player():
    gameover = False
    # TODO: highscore

    # Initializing bird sprite
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Bird())
    bird = player_group.sprite # Reference/pointer to player bird

    score = 0
    pipes = []
    next_pipe = None

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
            if event.type == pipe_timer and bird.alive:
                pipes.append(Pipe(WIN_WIDTH))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_player()
                if event.key == pygame.K_m:
                    menu_main()



        # Background: movement + draw
        if bird.alive: bg_group.update()
        bg_group.draw(screen)

        # Player bird: movement + draw
        player_group.update(events)
        player_group.draw(screen)

        pipes_to_remove = []

        for pipe in pipes:

            if bird.alive: # Move pipe if bird is alive
                pipe.update()

            if  pipe.top_pipe.rect.right < 0:
                pipes_to_remove.append(pipe) # Remove pipe when out of screen

            # Collision
            if (bird.alive and
                    (pygame.sprite.collide_mask(player_group.sprite, pipe.top_pipe) or
                     pygame.sprite.collide_mask(player_group.sprite, pipe.bottom_pipe))): # TODO: optimize, new mask each time
                player_group.sprite.alive = False
                utils.audio_hit.play()
                utils.audio_die.play()

            # Scoring
            if pipe.passed and not pipe.scored: # Only score once per pipe
                score += 1
                pipe.scored = True
                utils.audio_point.play()

            pipe.draw(screen)

        # Ground: movement + draw
        if bird.alive: ground_group.update()
        ground_group.draw(screen)

        # Ground collision
        for ground_sprite in ground_group.sprites():
            # Bird dies to floor
            if bird.alive and pygame.sprite.collide_mask(player_group.sprite, ground_sprite): # TODO: optimize, new mask each time
                player_group.sprite.alive = False
                utils.audio_hit.play()

            # Gameover: when the bird hits the floor
            if pygame.sprite.collide_mask(player_group.sprite, ground_sprite): # TODO: optimize, new mask each time
                gameover = True

        # Sky collision (out of bounds)
        if bird.rect.centery <= 0 and bird.alive:
            utils.audio_die.play()
            bird.alive = False

        for pipe_to_remove in pipes_to_remove: # Removing off-screen pipes
            pipes.remove(pipe_to_remove)

        if gameover:
            display_gameover(score, events)
            display_stats(None, fps, None)
        else:
            display_stats(score, fps, None)

        pygame.display.update()
        clock.tick(MAX_FRAME_RATE) # Setting max framerate

def display_gameover(score, events):
    gameover = pygame.transform.scale_by(pygame.image.load(get_asset_path("images", "menu", "gameover.png")), 2).convert_alpha()
    gameover_rect = gameover.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y - 300))

    score_shadow = utils.get_shadow_font(13, f"Score: {score}", utils.Font.FB,
                                           False, (255, 255, 255), (0, 0, 0),
                                           (WIN_CENTER_X, WIN_CENTER_Y - 200))

    highscore_shadow = utils.get_shadow_font(13, f"HighScore: {score}", utils.Font.FB,
                                         False, (255, 255, 255), (0, 0, 0),
                                         (WIN_CENTER_X, WIN_CENTER_Y - 100))

    restart_button = Button("Restart", 15, (WIN_CENTER_X, WIN_CENTER_Y + 50), game_player)
    menu_button = Button("Menu", 12, (WIN_CENTER_X, WIN_CENTER_Y + 150), menu_main)

    button_group = pygame.sprite.Group(
        restart_button,
        menu_button
    )

    button_group.update(screen, events)
    button_group.draw(screen)


    screen.blit(gameover, gameover_rect)

    screen.blit(score_shadow["shadow"]["surf"], score_shadow["shadow"]["rect"])
    screen.blit(score_shadow["base"]["surf"], score_shadow["base"]["rect"])

    screen.blit(highscore_shadow["shadow"]["surf"], highscore_shadow["shadow"]["rect"])
    screen.blit(highscore_shadow["base"]["surf"], highscore_shadow["base"]["rect"])

# # # # # # # # # # # # # # # ARTIFICIAL INTELLIGENCE GAME # # # # # # # # # # # # # # #

def game_ai():
    # TODO: mute volume until a certain threshold of birds left
    # if next_pipe != None:
    #     pygame.draw.line(screen, (255, 0, 0), bird.rect.center,
    #                      next_pipe.top_pipe.rect.midbottom)
    #     pygame.draw.line(screen, (255, 0, 0), bird.rect.center,
    #                      next_pipe.bottom_pipe.rect.midtop)
    # for pipe in pipes:
    #     if pipe.top_pipe.rect.centerx > Bird.BIRD_X:
    #         next_pipe = pipe
    #         break
    pass

# # # # # # # # # # # # # # # ENTRY POINT # # # # # # # # # # # # # # #
def main():
    # utils.audio_die.play(loops = -1)
    menu_main()

if __name__ == "__main__":
    main()
