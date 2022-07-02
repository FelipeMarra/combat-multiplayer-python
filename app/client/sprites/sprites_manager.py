import pygame
import os

from app import *

def update_sprites(game):
    game.all_sprites.update()

def draw_sprites(game):
    # cleaning screen
    game.screen.fill(BLACK)
    game.map_background = os.path.join(game.maps_directory, f"map{game.map}background.png")
    game.map_background = pygame.image.load(game.map_background).convert_alpha()
    game.map_background = pygame.transform.smoothscale(game.map_background, (WIDTH, HEIGHT))
    game.screen.blit(game.map_background, game.map_background.get_rect())
    # drawing sprits
    game.all_sprites.draw(game.screen)
    #draw pointer
    pygame.mouse.set_visible(False)
    game.pointerImg_rect = game.pointerImg.get_rect()
    game.pointerImg_rect.center = pygame.mouse.get_pos()
    game.screen.blit(game.pointerImg, game.pointerImg_rect)
    pygame.display.flip()