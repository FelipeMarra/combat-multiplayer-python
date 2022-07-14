import pygame as pg
from app import *

class Wall(pg.sprite.Sprite):
    def __init__(self, pos, size, map):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(size)
        self.image.fill(COLORS[map-1])
        self.rect = self.image.get_rect()
        self.rect.center = pos

def wall_creator(game, map):
    if map==1:
        wall = Wall((200, HEIGHT/2), (15, 300), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((WIDTH - 200, HEIGHT/2), (15, 300), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((350, HEIGHT/2), (50, 50), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((WIDTH - 350, HEIGHT/2), (50, 50), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((475, (HEIGHT/4)*1), (80, 25), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((475, (HEIGHT/4)*3), (80, 25), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((WIDTH - 475, (HEIGHT/4)*1), (80, 25), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((WIDTH - 475, (HEIGHT/4)*3), (80, 25), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
    if map==2:
        wall = Wall((200, HEIGHT/2), (15, 300), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)
        
        wall = Wall((WIDTH - 200, HEIGHT/2), (15, 300), map)
        game.walls.add(wall)
        game.all_sprites.add(wall)