from socket import *
import pickle
from player_data import *
from constants import *

class Network:
    def __init__(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.server = ip
        self.port = port
        self.buffer = 1024
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


    def send(self, server_pkt):
        try:
            #sending object
            self.client.send(pickle.dumps(server_pkt))
            #In case we're sending our player update we want to get others back
            return pickle.loads(self.client.recv(self.buffer))
        except error:
            print(f"Error sending pkt type {type(error)}")