import sys
from socket import *
import threading

import pickle

from app import *

class Server:
    def __init__(self):
        self.players_sockets = []
        self.ready_players = []
        self.initial_player_data = []
        self.game_map = -1
        self.serverSocket = None
    
    def send_all(self, server_pkt):
        for player_socket in self.players_sockets:
            player_socket.send(pickle.dumps(server_pkt))

    def send_others(self, client_socket, server_pkt):
        for player_socket in self.players_sockets:
            if(player_socket != client_socket):
                player_socket.send(pickle.dumps(server_pkt))

    #Create Server and return server socket
    def start(self, server_port):
        try:
            server_socket = socket(AF_INET, SOCK_STREAM)
            server_socket.bind(("", int(server_port)))
            server_socket.listen(1)
            print(f"Server ready at port {server_port}, {gethostbyname(gethostname())}")
            print()

            self.serverSocket = server_socket;

            self.handle_connections()
        except:
            raise Exception("Can't create server")

    def handle_connections(self):
        while True:
            #Não aceitar mais que dois players
            if(len(self.players_sockets) <= 1):
                try:
                    clientSocket, addr = self.serverSocket.accept()
                except:
                    print("Error accepting")
                    quit()

                new_thread = threading.Thread(target=self.listen_client, args=(clientSocket, addr, len(self.players_sockets)))
                new_thread.start()

                self.players_sockets.append(clientSocket)
                
    def listen_client(self, client_socket, addr, pid):
        #If there's no other player pid is 0
        if(pid == 0):
            print(f"Client {addr} started a new game.")
            player = PlayerData(pid, PLAYER_POSITION_0)
            self.initial_player_data.append(player)
            client_socket.send(pickle.dumps(player))
            print("Awaiting next player")
        #If there is another player pid is 1
        elif(pid == 1):
            print(f"Client {addr} entered the game.")
            player = PlayerData(pid, PLAYER_POSITION_1)
            self.initial_player_data.append(player)
            client_socket.send(pickle.dumps(player))
            self.ready_players.append(player)
            print("Player 1 is ready")
            #send to first player that a new player entered the game
            self.players_sockets[0].send(pickle.dumps(player))
            print("Game Started!!!")

        while True:
            try:
                data = client_socket.recv(BUFFER_SIZE)
                if data:
                    server_pkt = pickle.loads(data)
                    if server_pkt:
                        #Send my update to all other players
                        if type(server_pkt) is PlayerData:
                            self.send_others(client_socket, server_pkt)

                        elif type(server_pkt) is BulletData:
                            self.send_all(server_pkt)

                        #if its not a class is a string command 
                        elif type(server_pkt) is Command:
                            #Game Map
                            if(server_pkt.type == POST_GAME_MAP):
                                print(f"Player {server_pkt.data} selecionou o mapa {server_pkt.data}")
                                self.game_map = server_pkt.data

                            if(server_pkt.type == GET_GAME_MAP):
                                client_socket.send(pickle.dumps(self.game_map))

                            #Game Ready
                            if(server_pkt.type == GET_READY_PLAYERS):
                                client_socket.send(pickle.dumps(self.ready_players))

                            if(server_pkt.type == POST_PID_IS_READY):
                                print(f"Player {server_pkt.data} disse que esta pronto")
                                pickle.dumps(self.ready_players.append(server_pkt.data))

                            #Get other players
                            if(server_pkt.type == GET_INTIAL_ENEMY_PLAYER):
                                other_player = (pid + 1) % 2
                                print(f"{pid} SENDING OTHER PLAYER DATA ({self.initial_player_data[other_player]}) TO {other_player}")
                                client_socket.send(pickle.dumps(self.initial_player_data[other_player]))

                            #Game reset
                            if(server_pkt.type == POST_GAME_RESET):
                                print(f"{pid} SENT A RESET WITH LIFE = {server_pkt.data[1]}")
                                self.send_all(server_pkt)

            except error:
                print(f"Erro ao ouvir cliente {addr}: {type(error)}: {error.args}")
                break
        #If one player goes off, all of them must go off too
        #TODO THIS PART IS NOT WORKING
        for socket in self.players_sockets:
            socket.close()
        self.players_sockets.clear()


if __name__ == "__main__":
    file, server_port = sys.argv
    server = Server()
    server.start(int(server_port))