import pygame as pg
vec = pg.math.Vector2
from app.global_constants import *

class Command():
    def __init__(self, type, data = None):
        self.type = type
        self.data = data

class PlayerData():
    def __init__(self, pid, initial_position):
        self.pid = pid
        self.pos = initial_position
        self.vel = (0, 0)
        self.acc = (0, 0)
        self.angle = 0
        self.life = 3

class BulletData():
    def __init__(self, pos, dir, dx, dy, pid):
        self.pos = pos
        self.dir = dir
        self.dx = dx
        self.dy = dy
        self.pid = pid