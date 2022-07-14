from socket import *
import ctypes
import pickle

import threading

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

    def send_pid_is_ready(self):
        self.client.send(pickle.dumps(Command(POST_PID_IS_READY, self.my_player_data)))

    def send_selected_map(self, selected_map):
        self.client.send(pickle.dumps(Command(POST_GAME_MAP, selected_map)))

    def send_game_reset(self):
        self.client.send(pickle.dumps(Command(POST_GAME_RESET, (self.my_player_data.pid, self.my_player_data.life))))

    def send_bullet_data(self, bullet_data):
        self.client.send(pickle.dumps(bullet_data))

    def send_player_data(self, bullet_data):
        self.client.send(pickle.dumps(bullet_data))

    def start_receive(self, game):
            new_thread = threading.Thread(target=self.receive, args=(id(game),))
            new_thread.start()

    def receive(self, game):
        game = ctypes.cast(game, ctypes.py_object).value
        while game.state != END_STATE:
            if(game.state == GET_MAP_STATE):
                self.client.send(pickle.dumps(Command(GET_GAME_MAP)))
                data = self.client.recv(BUFFER_SIZE)
                game_map = pickle.loads(data)

                if(type(game_map) == int):
                    if(game_map != -1):
                        game.map = game_map
                        print(f"PLAYER {self.my_player_data.pid} RECEBEU O MAPA {game.map}")
                        game.state = AWAIT_PLAYERS_STATE

            if(game.state == AWAIT_PLAYERS_STATE):
                self.client.send(pickle.dumps(Command(GET_READY_PLAYERS)))
                data = self.client.recv(BUFFER_SIZE)
                players = pickle.loads(data)

                if(type(players) == list):
                    if(len(players) == N_PLAYERS):
                        print(f"PLAYER {self.my_player_data.pid} SAID GAME IS READY")
                        self.enemy_player_data = [x for x in players if x.pid != self.my_player_data.pid][0]
                        game.state = TRADE_UPDATES_STATE

            if(game.state == TRADE_UPDATES_STATE):
                #try:
                    data = self.client.recv(BUFFER_SIZE)

                    if data:
                        server_pkt = pickle.loads(data)
                        
                        if type(server_pkt) is PlayerData and hasattr(game, 'enemy_player'):
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
                                if(server_pkt.data[0] != self.my_player_data.pid):
                                    self.enemy_player_data.life = server_pkt.data[1]
                                    game.enemy_player.life = server_pkt.data[1]
                                game.reset()
                # except:
                #     print("ERROR RECEIVING ON TRADING STATE")
        print("MATOU A NETWORK")
