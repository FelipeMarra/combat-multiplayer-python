import pygame as pg
from app import *

class Wall(pg.sprite.Sprite):
    def __init__(self, pos, size):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(size)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = pos

def wall_creator(game, map):
    if map==1:
        wall = Wall((200, HEIGHT/2), (15, 300))
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((WIDTH - 200, HEIGHT/2), (15, 300))
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((350, HEIGHT/2), (50, 50))
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((WIDTH - 350, HEIGHT/2), (50, 50))
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((475, (HEIGHT/4)*1), (80, 25))
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((475, (HEIGHT/4)*3), (80, 25))
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((WIDTH - 475, (HEIGHT/4)*1), (80, 25))
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((WIDTH - 475, (HEIGHT/4)*3), (80, 25))
        game.walls.add(wall)
        game.all_sprites.add(wall)