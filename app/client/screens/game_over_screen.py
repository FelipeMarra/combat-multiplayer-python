import pygame
from app import *
import os

import app.client.screens.screen_utils as screen

def get_font(game, font_size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(game.font, font_size)

def show(game):
    win = 0
    if game.my_player.life != 0: 
        win = 1
            
    game.endsong = pygame.mixer.Sound(os.path.join(game.audios_directory, f"gameoversong{win}.wav"))
    game.endsong.set_volume(0.5)
    game.endsong.play(-1)
    
    SCREEN = game.screen
    SCREEN.fill(BLACK)
    
    game.morpheus_reaction = os.path.join(game.morpheus_diretory, f"morpheus{win}.jpg")
    game.morpheus_reaction = pygame.image.load(game.morpheus_reaction).convert_alpha()
    game.morpheus_reaction = pygame.transform.smoothscale(game.morpheus_reaction, (WIDTH, HEIGHT))
    SCREEN.blit(game.morpheus_reaction, game.morpheus_reaction.get_rect())
    
    waiting = True

    while waiting:
        text = "YOU ARE A LOSER?" if win == 0 else "CONGRATULATIONS?" 

        PLAY_TEXT = get_font(game, 45).render(text, True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(WIDTH/2, HEIGHT - 80))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        
        text2 = "WHAT IF I TOLD YOU" 

        PLAY_TEXT2 = get_font(game, 45).render(text2, True, "White")
        PLAY2_RECT = PLAY_TEXT2.get_rect(center=(WIDTH/2, 80))
        SCREEN.blit(PLAY_TEXT2, PLAY2_RECT)
        
        '''
        map_1_button = screen.Button(image=None, pos=(450, 450), text_input="GoodBye!", 
                                font=get_font(game, 75), base_color="Blue", hovering_color="Red")


        map_1_button.changeColor(mouse_position)
        map_1_button.update(SCREEN)
        '''
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type ==  pygame.MOUSEBUTTONDOWN:
                game.endsong.stop()
                pygame.quit()
                waiting = False
                game.state = END_STATE
                os._exit()

        pygame.display.update()