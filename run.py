import sys
import getopt
import socket
import subprocess
import threading

LOCAL_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 6666
N_CLIENTS = 2

def run_server():
    command = f"python -m app.server.server {SERVER_PORT}"
    subprocess.call(command, creationflags=subprocess.CREATE_NEW_CONSOLE)


def run_client():
    command = f"python -m app.client.client {LOCAL_IP} {SERVER_PORT}"
    subprocess.call(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    argumentList = sys.argv[1:]

    # Options
    options = "cs"

    # Long options
    long_options = ["client-only", "server-only"]

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        if(len(arguments) == 0):
            server_thread = threading.Thread(target=run_server)
            server_thread.start()

            for n in range(N_CLIENTS):
                client_thread = threading.Thread(target=run_client)
                client_thread.start()

        else:
            # checking each argument
            for currentArgument, currentValue in arguments:

                if currentArgument in ("-c", "--client-only"):
                    client_thread = threading.Thread(target=run_client)
                    client_thread.start()

                elif currentArgument in ("-s", "--server-only"):
                    server_thread = threading.Thread(target=run_server)
                    server_thread.start()

    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))