import pygame
from app import *

import app.client.screens.screen_utils as screen

def show(game):
    game.start_song.play(-1)
    font_fade = pygame.USEREVENT + 1
    show_text = True
    pygame.time.set_timer(font_fade, 900)

    waiting = True
    while waiting:
        game.timer.tick(120)

        # show texts
        for event in pygame.event.get():
            # await command
            if event.type == pygame.QUIT:
                waiting = False
                game.is_running = False

            if event.type == pygame.KEYUP:
                game.beep_sound.play()
                game.start_song.stop()
                waiting = False

            # blinking text
            if event.type == font_fade:
                show_text = not show_text

            game.screen.fill(BLACK)
            game.start_background_rect = game.start_background.get_rect()
            game.screen.blit(game.start_background, game.start_background_rect)

            # show logo
            start_logo_rect = game.start_logo.get_rect()
            start_logo_rect.midtop = (WIDTH / 2, 20)
            game.screen.blit(game.start_logo, start_logo_rect)

            # show tanks
            wallpaper1_tank_rect = game.tank_wallpaper1.get_rect()
            wallpaper1_tank_rect.midtop = (200, 250)
            game.screen.blit(game.tank_wallpaper1, wallpaper1_tank_rect)

            wallpaper2_tank_rect = game.tank_wallpaper2.get_rect()
            wallpaper2_tank_rect.midtop = (WIDTH - 200, HEIGHT - 470)
            game.screen.blit(game.tank_wallpaper2, wallpaper2_tank_rect)

            if show_text:
                screen.show_text(game, 'PRESS ANY KEY TO CONNECT', 32, YELLOW, WIDTH / 2, HEIGHT / 2 + 50)

            screen.show_text(game, 'Developed by Marra & Galli & Furi', 19, WHITE, WIDTH / 2, HEIGHT - 20)
            pygame.display.flip()