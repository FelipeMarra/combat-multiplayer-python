import pygame
from app import *

import app.client.screens.screen_utils as screen

def show(game):
    font_fade = pygame.USEREVENT + 1
    show_text = True
    pygame.time.set_timer(font_fade, 900)

    game.screen.fill(BLACK)
    waiting = True

    while waiting:
        game.timer.tick(120)

        if game.state == TRADE_UPDATES_STATE:
            waiting = False
            return

        # show texts
        for event in pygame.event.get():
            # await command
            if event.type == pygame.QUIT:
                waiting = False
                game.state = END_STATE

            # blinking text
            if event.type == font_fade:
                show_text = not show_text

            if show_text:
                screen.show_text(game, 'WAITING THE OPPONENT', 32, WHITE, WIDTH / 2, HEIGHT / 2 + 50)

            pygame.display.flip()