import pygame
from app import *
import os

import app.client.screens.screen_utils as screen

def get_font(game, font_size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(game.font, font_size)

def show(game):
    SCREEN = game.screen
    waiting = True

    while waiting:
        mouse_position = pygame.mouse.get_pos()

        SCREEN.fill(BLACK)

        text = "Game Over" if game.my_player.life == 0 else "You Win" 

        PLAY_TEXT = get_font(game, 45).render(text, True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        map_1_button = screen.Button(image=None, pos=(200, 460), text_input="Go To Initial Screen", 
                                font=get_font(game, 75), base_color="White", hovering_color="Red")

        map_1_button.changeColor(mouse_position)
        map_1_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting = False
                game.is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if map_1_button.checkForInput(mouse_position):
                    waiting = False
                    game.state = END_STATE
                    return 1

        pygame.display.update()