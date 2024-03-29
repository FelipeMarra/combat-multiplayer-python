import pygame
from app import *
import os

import app.client.screens.screen_utils as screen

def get_font(game, font_size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(game.font, font_size)

def show(game):
    SCREEN = game.screen
    game.morpheus.play(-1)
    waiting = True

    while waiting:
        mouse_position = pygame.mouse.get_pos()

        game.screen.fill(BLACK)
        game.choicemap_rect = game.choicemap.get_rect()
        game.screen.blit(game.choicemap, game.choicemap_rect)

        PLAY_TEXT = get_font(game, 45).render("REDPILL OR BLUE PILL?", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        map_1_button = screen.Button(image=None, pos=(400, 420), 
                            text_input="MAP 1", font=get_font(game, 75), base_color="White", hovering_color="Red")
        
        map_2_button = screen.Button(image=None, pos=(WIDTH - 400, 430), 
                            text_input="MAP 2", font=get_font(game, 75), base_color="White", hovering_color="Blue")
        

        map_2_button.changeColor(mouse_position)
        map_2_button.update(SCREEN)

        map_1_button.changeColor(mouse_position)
        map_1_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting = False
                game.is_running = False
                game.morpheus.stop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if map_1_button.checkForInput(mouse_position):
                    game.network.send_pid_is_ready()
                    waiting = False
                    game.morpheus.stop()
                    return 1


                if map_2_button.checkForInput(mouse_position):
                    game.network.send_pid_is_ready()
                    waiting = False
                    game.morpheus.stop()
                    return 2


        pygame.display.update()