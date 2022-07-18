import math
from app import *
import pygame as pg

vec = pg.math.Vector2

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, dx, dy, pid):
        pg.sprite.Sprite.__init__(self)
        self.dx = dx
        self.dy = dy
        self.dir_x, self.dir_y = pg.mouse.get_pos()
        self.dir = dir
        self.pid = pid
        self.game = game
        if self.pid == 0:
            self.image = self.game.blue_bullet
        if self.pid == 1:
            self.image = self.game.red_bullet
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = self.dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.rotate()
        self.channel = pg.mixer.find_channel()
        self.play_sound(self.game.bullet_song)
        self.bounced = list()

    def rotate(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pg.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.pos)

    def play_sound(self, song):
        self.channel.get_queue()
        self.channel.play(song)

    def bounce(self, direction):
        if direction == LATERAL:
            self.dx = -self.dx
        elif direction == UPDOWN:
            self.dy = -self.dy
        self.dir = vec(self.dx, self.dy)
        self.vel = self.dir * BULLET_SPEED

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

        
        
        # hit the border and go the other way
        if self.pos.x > WIDTH or self.pos.x < 0:
            # hit the lateral of the screen
            self.bounce(LATERAL)
            
        if self.pos.y < 0 or self.pos.y > HEIGHT:
            # hit up or down in the screen
            self.bounce(UPDOWN)
            
        #bounce in the walls 
        walls_hit = pg.sprite.spritecollide(self, self.game.walls, False)
        for wall in walls_hit:
            if abs(wall.rect.top - self.rect.bottom) < BULLET_COLLISION_TOLLERANCE:
                self.bounce(UPDOWN)
            if abs(wall.rect.bottom - self.rect.top) < BULLET_COLLISION_TOLLERANCE:
                self.bounce(UPDOWN)
            if abs(wall.rect.right - self.rect.left) < BULLET_COLLISION_TOLLERANCE:
                self.bounce(LATERAL)
            if abs(wall.rect.left - self.rect.right) < BULLET_COLLISION_TOLLERANCE:
                self.bounce(LATERAL)

        if pg.sprite.spritecollide(self.game.enemy_player, self.game.alliebullets, False):
            self.game.enemy_player.explode(bullet=self)

        if pg.sprite.spritecollide(self.game.my_player, self.game.enemybullets, False):
            #run explosion animation
            self.game.my_player.explode(bullet=self)

    def add(data, game):
        b = Bullet(game, data.pos, data.dir, data.dx, data.dy, data.pid)

        if data.pid == game.my_player.pid:
            game.alliebullets.add(b)
        else:
            game.enemybullets.add(b)

        game.all_sprites.add(b)