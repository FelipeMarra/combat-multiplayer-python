from constants import *
import pygame as pg
from player_data import *
import os
import math

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, data:PlayerData, itsMe:bool):
        pg.sprite.Sprite.__init__(self)
        self.pid = data.pid
        self.game = game
        if self.pid == 0:
            self.image = self.game.player_image
        elif self.pid == 1:
            self.image = self.game.enemy_image
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = data.pos
        self.pos = vec(data.pos)
        self.vel = vec(data.vel)
        self.acc = vec(data.acc)
        self.last_shot = -BULLET_RATE
        self.channel = pg.mixer.find_channel()
        self.itsMe = itsMe
        

    def rotate(self, angle = None):
        if not angle:
            mouse_x, mouse_y = pg.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pg.transform.rotate(self.original_image, int(angle))
            self.rect = self.image.get_rect(center=self.pos)
            return angle
        if angle:
            self.image = pg.transform.rotate(self.original_image, int(angle))
            self.rect = self.image.get_rect(center=self.pos)

    def get_mouse_vector(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = math.atan2(rel_y, rel_x)
        dx = math.cos(angle) * BULLET_SPEED
        dy = math.sin(angle) * BULLET_SPEED
        return dx, dy

    def play_sound(self, song):
        self.channel.get_queue()
        self.channel.play(self.game.engine_run)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > BULLET_RATE:
            self.last_shot = now
            dx, dy = self.get_mouse_vector()
            dir = vec(dx, dy)
            pos = self.pos + dir
            b = Bullet(self.game, pos, dir, dx, dy, self.pid)
            #Send to server
            self.game.network.send(ServerPkt(BULLET, BulletData(pos, dir, dx, dy, self.pid)))
            self.game.all_sprites.add(b)
            self.game.alliebullets.add(b)

    def update(self):
        ####### position #########
        if self.itsMe:
            self.acc = vec(0, 0)
            keys = pg.key.get_pressed()
            if (keys[pg.K_LEFT] or keys[pg.K_a]) and self.pos.x > 25:
                self.acc.x = -PLAYER_ACC
            if (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.pos.x < WIDTH - 25:
                self.acc.x = PLAYER_ACC
            if( keys[pg.K_UP] or keys[pg.K_w]) and self.pos.y > 25:
                self.acc.y = -PLAYER_ACC
            if (keys[pg.K_DOWN] or keys[pg.K_s]) and self.pos.y < HEIGHT - 25:
                self.acc.y = PLAYER_ACC
            if pg.mouse.get_pressed()[0]:
                self.shoot()

            # apply friction
            self.acc += self.vel * PLAYER_FRICTION
            # equations of motion
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            self.rect.center = self.pos
            angle = self.rotate()

            self.game.network.my_player_data.pos = self.pos
            self.game.network.my_player_data.vel = self.vel
            self.game.network.my_player_data.acc = self.acc
            self.game.network.my_player_data.angle = angle

            #send update to server
            self.game.network.send(ServerPkt(PLAYER, self.game.network.my_player_data))

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, dx, dy, pid):
        pg.sprite.Sprite.__init__(self)
        self.dx = dx
        self.dy = dy
        self.dir_x, self.dir_y = pg.mouse.get_pos()
        self.dir = dir
        self.pid = pid
        self.game = game
        self.image = self.game.blue_bullet
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = self.dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.rotate()
        self.channel = pg.mixer.find_channel()
        self.play_sound(self.game.bullet_song)

    def rotate(self, hitting=False):
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

        # hit the wall and go the other way
        if self.pos.x > WIDTH or self.pos.x < 0:
            # hit the lateral of the screen
            self.bounce(LATERAL)

        if self.pos.y < 0 or self.pos.y > HEIGHT:
            # hit up or down in the screen
            self.bounce(UPDOWN)

class Wall(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)