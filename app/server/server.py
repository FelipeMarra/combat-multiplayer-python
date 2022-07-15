import logging
import sys
from socket import *
import threading

import pickle

from app import *

class Server:
    def __init__(self):
        self.players_sockets = []
        self.ready_players = []
        self.game_map = -1
        self.serverSocket = None

    def clear(self):
        print("SERVER WAS CLEARED")
        self.players_sockets.clear()
        self.ready_players.clear()
        self.game_map = -1

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
            print(f"SERVER READY AT PORT {server_port}, {gethostbyname(gethostname())}")

            self.serverSocket = server_socket;

            self.handle_connections()
        except BaseException:
            logging.exception(f"Error on start server:")

    def handle_connections(self):
        while True:
            #Não aceitar mais que dois players
            if(len(self.players_sockets) <= 1):
                try:
                    clientSocket, addr = self.serverSocket.accept()
                except BaseException:
                    logging.exception(f"Error accepting {addr}:")
                    quit()

                new_thread = threading.Thread(target=self.listen_client, args=(clientSocket, addr, len(self.players_sockets)))
                new_thread.start()

                self.players_sockets.append(clientSocket)

    def listen_client(self, client_socket, addr, pid):
        #If there's no other player pid is 0
        if(pid == 0):
            print(f"CLIENT {addr} STARTED A NEW GAME.")
            player = PlayerData(pid, PLAYER_POSITION_0)
            client_socket.send(pickle.dumps(player))
            print("AWAITING NEXT PLAYER")
        #If there is another player pid is 1
        elif(pid == 1):
            print(f"CLIENT {addr} ENTERED THE GAME.")
            player = PlayerData(pid, PLAYER_POSITION_1)
            client_socket.send(pickle.dumps(player))
            #send to first player that a new player entered the game
            self.players_sockets[0].send(pickle.dumps(player))

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
                                print(f"PLAYER {pid} SELECTED MAP {server_pkt.data}")
                                self.game_map = server_pkt.data

                            if(server_pkt.type == GET_GAME_MAP):
                                client_socket.send(pickle.dumps(self.game_map))

                            #Game Ready
                            if(server_pkt.type == GET_READY_PLAYERS):
                                client_socket.send(pickle.dumps(self.ready_players))

                            if(server_pkt.type == POST_PID_IS_READY):
                                print(f"PLAYER {server_pkt.data.pid} IS READY")
                                self.ready_players.append(server_pkt.data)

                            #Game reset
                            if(server_pkt.type == POST_GAME_RESET):
                                print(f"{pid} SENT A RESET WITH LIFE = {server_pkt.data[1]}")
                                self.send_all(server_pkt)
                                #If a player have lost disconect all to reset the game
                                if(server_pkt.data[1] == 0):
                                    break

            except BaseException:
                logging.exception(f"Error listening to client {addr}:")
                break

        #If one player goes off, all of them must go off too
        for socket in self.players_sockets:
            try:
                socket.close()
            except:
                pass

        self.clear()


if __name__ == "__main__":
    file, server_port = sys.argv
    server = Server()
    server.start(int(server_port))