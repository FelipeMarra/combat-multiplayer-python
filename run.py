import os
import socket
import threading

LOCAL_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 6666
TEST_MODE = "True"
N_CLIENTS = 2

def run_server():
    os.popen(f"python app/server/server.py {SERVER_PORT}")

def run_client():
    os.popen(f"python app/client/client.py {LOCAL_IP} {SERVER_PORT} {TEST_MODE}")

if __name__ == "__main__":
    run_server()

    for n in range(N_CLIENTS):
        run_client()