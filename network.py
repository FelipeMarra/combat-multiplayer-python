from socket import *
import pickle
from player_data import *
from constants import *
import ctypes

class Network:
    def __init__(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.server = ip
        self.port = port
        self.buffer = 1024*2
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
            server_pkt = pickle.loads(self.client.recv(self.buffer))
            my_player = server_pkt.data
            print(f"Received initial player obj pid: {my_player.pid}")
            self.my_player_data = my_player
            return my_player
        except:
            print(f"Error receiving intial player data")
            self.client.close()
            quit()

    #Quando o pacote do jodor tem id 0 precisamos aguardar para receber o prox
    def await_match(self):
        while True:
            try:
                data = self.client.recv(self.buffer)
                if(data):
                    server_pkt = pickle.loads(data)
                    if server_pkt:
                        self.enemy_player_data = server_pkt.data
                        return server_pkt.data
            except:
                print("Error on matchmaking")
                self.client.close()
                quit()

    def start_enemy(self, server_pkt):
        try:
            self.client.send(pickle.dumps(server_pkt))
            #In case we're sending our player update for the first time we want to get others back
            return pickle.loads(self.client.recv(self.buffer)).data
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
                data = self.client.recv(self.buffer)
                if data:
            
                    try:
                        server_pkt = pickle.loads(data)
                    except:
                        #Pickle raises exception when moving game window borders
                        pass

                    if server_pkt.type == PLAYER:
                        enemy_data = server_pkt.data
                        game.network.enemy_player_data = enemy_data
                        game.enemy_player.pos = game.network.enemy_player_data.pos
                        game.enemy_player.vel = game.network.enemy_player_data.vel
                        game.enemy_player.acc = game.network.enemy_player_data.acc
                        game.enemy_player.angle = game.network.enemy_player_data.angle
                        game.enemy_player.rect.center = game.enemy_player.pos
                        game.enemy_player.rotate(game.enemy_player.angle)

            except error:
                print(f"Error on network receive")