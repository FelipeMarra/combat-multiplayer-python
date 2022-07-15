import pygame
from app import *
import os

import app.client.screens.screen_utils as screen

def get_font(game, font_size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(game.font, font_size)

def show(game):
    pygame.mouse.set_visible(True)
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
        mouse_position = pygame.mouse.get_pos()
        text = "YOU ARE A LOSER?" if win == 0 else "CONGRATULATIONS?" 

        PLAY_TEXT = get_font(game, 75).render(text, True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(WIDTH/2, HEIGHT - 80))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        
        text2 = "WHAT IF I TOLD YOU" 

        PLAY_TEXT2 = get_font(game, 75).render(text2, True, "White")
        PLAY2_RECT = PLAY_TEXT2.get_rect(center=(WIDTH/2, 80))
        SCREEN.blit(PLAY_TEXT2, PLAY2_RECT)
        
        button_image = pg.Surface((100, 80))
        button_image.fill(BLACK)
        
        
        map_1_button = screen.Button(image=button_image, pos=(round((WIDTH/3)*1), HEIGHT/2), text_input="QUIT", 
                                font=get_font(game, 30), base_color="White", hovering_color="Blue")
        
        map_2_button = screen.Button(image=button_image, pos=(round((WIDTH/3)*2), HEIGHT/2), text_input="RESET", 
                                font=get_font(game, 30), base_color="White", hovering_color="Red")


        map_1_button.changeColor(mouse_position)
        map_1_button.update(SCREEN)
        
        map_2_button.changeColor(mouse_position)
        map_2_button.update(SCREEN)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game.endsong.stop()
                waiting = False
                game.state = END_STATE
                os._exit(1)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if map_1_button.checkForInput(mouse_position):
                    pygame.quit()
                    game.endsong.stop()
                    waiting = False
                    game.state = END_STATE
                    os._exit(1)
                
                if map_2_button.checkForInput(mouse_position):
                    game.endsong.stop()
                    waiting = False
                    game.state = END_STATE
                
        pygame.display.update()