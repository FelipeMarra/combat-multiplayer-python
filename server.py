from tkinter import E
from constants import *
import sys
import pickle
from socket import *
from player_data import *
import threading

class Server:
    def __init__(self):
        self.players_sockets = []
        self.serverSocket = None
        self.buffer = 1024

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
        print(f"CHEGOU UM CARA E A LEN DOS PLAYER EH {len(self.players_sockets)}")
        #If there's no other player pid is 0
        if(pid == 0):
            print(f"Client {addr} started a new game.")
            player = PlayerData(pid, PLAYER_POSITION_0)
            pkt = ServerPkt(PLAYER, player)
            client_socket.send(pickle.dumps(pkt))
            print("Awaiting next player")
        #If there is another player pid is 1
        elif(pid == 1):
            print(f"Client {addr} entered the game.")
            player = PlayerData(pid, PLAYER_POSITION_1)
            pkt = ServerPkt(PLAYER, player)
            client_socket.send(pickle.dumps(pkt))
            #send to first player that a new player entered the game
            self.players_sockets[0].send(pickle.dumps(pkt))
            print("Game Started!!!")
        
        #Se já ta rolando aquele joguin brabo
        while True:
            try:
                data = client_socket.recv(self.buffer)
                if data:
                    server_pkt = pickle.loads(data)
                    if server_pkt:
                        #Send my update to all other players
                        if server_pkt.type == PLAYER:
                            for player_socket in self.players_sockets:
                                if(player_socket != client_socket):
                                    player_socket.send(pickle.dumps(server_pkt.data))
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