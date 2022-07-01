import socket
import subprocess
import threading

LOCAL_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 6666
TEST_MODE = "True"
N_CLIENTS = 2

def run_server():
    command = f"python -m app.server.server {SERVER_PORT}"
    subprocess.call(command, creationflags=subprocess.CREATE_NEW_CONSOLE)


def run_client(cli_n):
    command = f"python -m app.client.client {LOCAL_IP} {SERVER_PORT} {TEST_MODE}"
    subprocess.call(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    for n in range(N_CLIENTS):
        client_thread = threading.Thread(target=run_client, args=(n,))
        client_thread.start()