from socket import *
import ctypes

import pickle

from app.server_models import *
from app.global_constants import *
from app.client.sprites import *

class Network():
    def __init__(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (ip, port)
        self.my_player_data = None
        self.enemy_player_data = None

    #Conecta ao servidor e recebe pacote correspondente ao jogador
    def connect(self):
        try:
            #conexão
            self.client.settimeout(5)
            self.client.connect(self.addr)
            self.client.settimeout(None)
        except:
            print(f"Error trying to connect")
            self.client.close()
            quit()

        try:
            #pacote do jogador
            my_player = pickle.loads(self.client.recv(BUFFER_SIZE))
            print(f"Received initial player obj pid: {my_player.pid}")
            self.my_player_data = my_player
            return my_player
        except:
            print(f"Error receiving intial player data")
            self.client.close()
            quit()

    #Envia para o servidor o comando que pede quantos jogadores estão prontos e retorna a resposta
    def get_game_is_ready(self):
        try:
            self.client.send(pickle.dumps(GET_GAME_IS_READY))
            data = self.client.recv(BUFFER_SIZE)
            if(data):
                n_ready = pickle.loads(data)
                return True if n_ready == 2 else False
        except:
            print(f"Error getting if game is ready")
            self.client.close()
            quit()

    def send_pid_is_ready(self):
        self.client.send(pickle.dumps(POST_PID_IS_READY))

    def start_enemy(self, server_pkt):
        try:
            self.client.send(pickle.dumps(server_pkt))
            #In case we're sending our player update for the first time we want to get others back
            return pickle.loads(self.client.recv(BUFFER_SIZE))
        except error:
            print(f"Error sending pkt type {type(error)}")

    def send(self, server_pkt):
        try:
            self.client.send(pickle.dumps(server_pkt))
        except error:
            print(f"Error sending pkt type {type(error)}")

    def receive(self, game):
        game = ctypes.cast(game, ctypes.py_object).value
        while True:
            try:
                data = self.client.recv(BUFFER_SIZE)
                if data:
            
                    try:
                        server_pkt = pickle.loads(data)
                    except:
                        #Pickle raises exception when moving game window borders
                        pass

                    if type(server_pkt) is PlayerData:
                        game.network.enemy_player_data = server_pkt
                        game.enemy_player.pos = game.network.enemy_player_data.pos
                        game.enemy_player.vel = game.network.enemy_player_data.vel
                        game.enemy_player.acc = game.network.enemy_player_data.acc
                        game.enemy_player.angle = game.network.enemy_player_data.angle
                        game.enemy_player.rect.center = game.enemy_player.pos
                        game.enemy_player.rotate(game.enemy_player.angle)
                    
                    if type(server_pkt) is BulletData:
                        b = Bullet(game, server_pkt.pos, server_pkt.dir, server_pkt.dx, server_pkt.dy, server_pkt.pid)
                        
                        if server_pkt.pid == game.my_player.pid:
                            game.alliebullets.add(b)
                        else:
                            game.enemybullets.add(b)
                        
                        game.all_sprites.add(b)
            except error:
                print(f"Error on network receive")
