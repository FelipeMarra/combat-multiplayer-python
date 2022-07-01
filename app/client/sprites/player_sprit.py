import math
import pygame as pg
from explosion_sprite import Explosion
from app import *

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
        self.channel.play(song)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > BULLET_RATE:
            self.last_shot = now
            dx, dy = self.get_mouse_vector()
            dir = vec(dx, dy)
            pos = self.pos
            #Send to server
            self.game.network.send(ServerPkt(BULLET, BulletData(pos, dir, dx, dy, self.pid)))
    
    def explode(self, bullet):
        if self in self.game.all_sprites.sprites():
            pos = vec((self.pos[0] + bullet.pos[0])/2,(self.pos[1] + bullet.pos[1])/2) 
            explosion = Explosion(self.game, pos)
            self.game.all_sprites.add(explosion)
            self.kill()
            bullet.kill()     
    
    def check_walls(self, direction):
        walls_hitten = pg.sprite.spritecollide(self, self.game.walls, False)
        for wall in walls_hitten:
            if (self.rect.right - wall.rect.left) < COLLISION_TOLLERANCE and direction == 'right':
                return True
            if (wall.rect.bottom -self.rect.top) < COLLISION_TOLLERANCE and direction == 'top':
                return True
            if (self.rect.bottom - wall.rect.top) < COLLISION_TOLLERANCE and direction == 'bottom':
                return True
            if (wall.rect.right -self.rect.left) < COLLISION_TOLLERANCE and direction == 'left':
                return True

    def update(self):
        ####### position #########
        if self.itsMe:                                
            self.acc = vec(0, 0)
            keys = pg.key.get_pressed()
            if (keys[pg.K_LEFT] or keys[pg.K_a]) and self.pos.x > 25 and not self.check_walls('left'):
                self.acc.x = -PLAYER_ACC
            if (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.pos.x < WIDTH - 25 and not self.check_walls('right'):
                self.acc.x = PLAYER_ACC 
            if( keys[pg.K_UP] or keys[pg.K_w]) and self.pos.y > 25 and not self.check_walls('top'):
                self.acc.y = -PLAYER_ACC
            if (keys[pg.K_DOWN] or keys[pg.K_s]) and self.pos.y < HEIGHT - 25 and not self.check_walls('bottom'):
                self.acc.y = PLAYER_ACC
            if (keys[pg.K_LSHIFT]):
                self.acc *= 2
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