import pygame as pg
vec = pg.math.Vector2
from constants import *

class ServerPkt():
    def __init__(self, type, data):
        self.type = type
        self.data = data

class PlayerData():
    def __init__(self, pid, initial_position):
        self.pid = pid
        self.pos = initial_position
        self.vel = (0, 0)
        self.acc = (0, 0)
        self.angle = 0

class BulletData():
    def __init__(self, pos, dir, dx, dy, pid):
        self.pos = pos
        self.dir = dir
        self.dx = dx
        self.dy = dy
        self.pid = pid

#Eu me conecto ao servidor
#peço meu Player Data
    #eu crio meu objeto player local
#eu fico esperando receber um novo player data que vai ser meu inimigo
    #eu crio o objeto desse novo playe
#a cada update meu
    #envio meu Player Data e o server joga esse update pros demais clients
#eu possuo um loop infinito que recebe updates de player data dos outros
    #a cada update do pid inimigo, eu atualiso o Player Data correspondente