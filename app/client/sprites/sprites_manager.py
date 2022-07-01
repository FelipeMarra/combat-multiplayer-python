import pygame

from app import *

def update_sprites(game):
    game.all_sprites.update()

def draw_sprites(game):
    # cleaning screen
    game.screen.fill(BLACK)
    game.screen.blit(game.map_background, game.map_background.get_rect())
    # drawing sprits
    game.all_sprites.draw(game.screen)
    #draw pointer
    pygame.mouse.set_visible(False)
    game.pointerImg_rect = game.pointerImg.get_rect()
    game.pointerImg_rect.center = pygame.mouse.get_pos()
    game.screen.blit(game.pointerImg, game.pointerImg_rect)
    pygame.display.flip()