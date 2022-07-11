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
    def get_game_is_ready(self, game):
        #TODO CONFLITO SEND/RECEIVE => MUDAR TODOS OS RECEIVE PRO MESMO LUGAR
        try:
            self.client.send(pickle.dumps(Command(GET_GAME_IS_READY)))
            data = self.client.recv(BUFFER_SIZE)
            game_map = pickle.loads(data)
            print(f"1 PLAYER {self.my_player_data.pid} RECEBEU O MAPA {game.map}")
            game.map = game_map
            return True if game_map != -1 else False
        except:
            print(f"Error getting if game is ready")
            self.client.close()
            quit()

    def send_pid_is_ready(self):
        self.client.send(pickle.dumps(Command(POST_PID_IS_READY, self.my_player_data.pid)))
    
    def send_selected_map(self, selected_map):
        self.client.send(pickle.dumps(Command(POST_GAME_MAP, selected_map)))

    def send_game_reset(self):
        self.client.send(pickle.dumps(Command(POST_GAME_RESET, self.my_player_data.pid)))
    
    def send_bullet_data(self, bullet_data):
        self.client.send(pickle.dumps(bullet_data))
    
    def send_player_data(self, bullet_data):
        self.client.send(pickle.dumps(bullet_data))

    def start_enemy(self):
        #TODO CONFLITO SEND/RECEIVE => MUDAR TODOS OS RECEIVE PRO MESMO LUGAR
        self.client.send(pickle.dumps(Command(GET_INTIAL_ENEMY_PLAYER)))
        data = self.client.recv(BUFFER_SIZE)
        enemy = pickle.loads(data)
        print(f"start_enemy: PLAYER {self.my_player_data.pid} recebeu {enemy}")
        return enemy

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
                        game.enemy_player.update_enemy()

                    if type(server_pkt) is BulletData:
                        b = Bullet(game, server_pkt.pos, server_pkt.dir, server_pkt.dx, server_pkt.dy, server_pkt.pid)
                        
                        if server_pkt.pid == game.my_player.pid:
                            game.alliebullets.add(b)
                        else:
                            game.enemybullets.add(b)
                        
                        game.all_sprites.add(b)

                    if type(server_pkt) is Command:
                        if(server_pkt.type == POST_GAME_RESET):
                            game.reset()

            except error:
                print(f"Error on network receive")
