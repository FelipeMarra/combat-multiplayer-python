import pygame

import app.client.client as client

# displays a text on the screen
def show_text(text, font_size, color, x, y):
    game = client.Game()
    font = pygame.font.Font(game.font, font_size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.midtop = (x, y)
    game.screen.blit(text, text_rect)