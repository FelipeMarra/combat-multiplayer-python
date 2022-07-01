import os
import pygame as pg
from app import *

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, pos):
        pg.sprite.Sprite.__init__(self)
        animation_directory = os.path.join(os.getcwd(), "midia/images/boom")
        self.game = game
        self.pos = pos
        self.images = []	
        self.channel = pg.mixer.find_channel()
        self.play_sound(self.game.explosion_sound)
        
        for num in range(1, 6):
            img = pg.image.load(os.path.join(animation_directory, f"exp{num}.png"))
            img = pg.transform.scale(img, (100,100))
            self.images.append(img)
            
        self.index = 0	
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.counter = 0

    def play_sound(self, song):
        self.channel.get_queue()
        self.channel.play(song)
        
    def update(self):
		#update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

		#if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= EXPLOSION_SPEED:
            self.kill()