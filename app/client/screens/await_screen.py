import pygame
from app import *
import threading

import app.client.screens.screen_utils as screen

def show(game):
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
                game.state = END_STATE

            # blinking text
            if event.type == font_fade:
                show_text = not show_text
                
            game.screen.fill(BLACK)
            game.waiting_image_rect = game.waiting_image.get_rect()
            game.screen.blit(game.waiting_image, game.waiting_image_rect)

            if show_text:
                screen.show_text(game, f'WAITING FOR OPPONENT', 32, PILLS[game.map - 1], WIDTH / 2, round(HEIGHT / 6))

            if game.state == TRADE_UPDATES_STATE:
                waiting = False
                return

            pygame.display.flip()