from constants import *
import pygame as pg
import os
import math
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.player_image
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.last_shot = -BULLET_RATE
        self.chanel = pg.mixer.find_channel()

    def rotate(self, hitting = False):
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if not hitting:
            self.image = pg.transform.rotate(self.original_image, int(angle))
        if hitting:
            self.image = pg.transform.rotate(self.original_image, int(-angle))
        self.rect = self.image.get_rect(center=self.pos)

    def get_mouse_vector(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = math.atan2(rel_y, rel_x)
        dx = math.cos(angle)*BULLET_SPEED
        dy = math.sin(angle)*BULLET_SPEED
        return dx, dy

    def play_sound(self, song):
        self.chanel.get_queue()
        self.chanel.play(self.game.engine_run)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > BULLET_RATE:
            self.last_shot = now
            dx, dy = self.get_mouse_vector()
            dir = vec(dx, dy)
            pos = self.pos + dir
            b = Bullet(self.game, pos, dir, dx, dy)
            b.sound()
            self.game.all_sprites.add(b)
            self.game.bullets.add(b)

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
        if pg.mouse.get_pressed()[0]:
            self.shoot()

        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos
        self.rotate()


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, dx, dy):
        self.dx = dx
        self.dy = dy
        self.dir_x, self.dir_y = pg.mouse.get_pos()
        self.dir = dir
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.bullet_img
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = self.dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.rotate()

    def rotate(self, hitting=False, mouse_x=None, mouse_y=None):
        if not hitting:
            mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if not hitting:
            self.image = pg.transform.rotate(self.original_image, int(angle))
        if hitting:
            self.image = pg.transform.rotate(self.original_image, int(-angle))

        self.rect = self.image.get_rect(center=self.pos)

    def sound(self):
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play()
        pg.mixer.music.fadeout(800)

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

        # hit the wall and go the other way
        statement1 = self.pos.x > WIDTH or self.pos.x < 0
        statement2 = self.pos.y < 0 or self.pos.y > HEIGHT
        if statement1:
            self.dir = vec(-self.dx, self.dy)
            self.vel = self.dir * BULLET_SPEED
            self.rotate(hitting=True, mouse_x=self.dir_x, mouse_y=self.dir_y)
        if statement2:
            self.dir = vec(self.dx, -self.dy)
            self.vel = self.dir * BULLET_SPEED
            self.rotate(hitting=True, mouse_x=self.dir_x, mouse_y=self.dir_y)
