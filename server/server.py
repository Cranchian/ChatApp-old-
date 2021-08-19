import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from mortal import Mortal

# Global Constants
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

# Global Variables
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # set up server
mortals = []  # client list


def broadcast(msg, name):
    """
    send new message to all clients
    :param msg: bytes['utf8']
    :param name: str
    :return:
    """
    for mortal in mortals:
        client = mortal.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]", e)


def client_communication(mortal):
    """
    Thread to handle all messages from client
    :param mortal: Mortal
    :return: None
    """
    client = mortal.client

    # get mortal's name (first message is always name)
    name = client.recv(BUFSIZ).decode("utf8")
    mortal.set_name(name)
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")  # broadcast welcome message

    # wait for messages from mortals
    while True:
        try:
            msg = client.recv(BUFSIZ)  # the message data received

            # if message is {quit} then close that client conn
            if msg == bytes("{quit}", "utf8"):
                client.close()
                mortals.remove(mortal)
                broadcast(bytes(f"{name} has left chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} disconnected")
                break

            # Else just send that message to everyone
            else:
                broadcast(msg, name+": ")
                print(f"{name}: ", msg.decode('utf8'))

        except Exception as e:
            print("[EXCEPTION]", e)
            break


def wait_for_connection():
    """
    Wait for connection from new clients, start new thread once connected
    :param SERVER: SOCKET
    :return: None
    """
    # wait for mortals to join the server
    while True:
        try:
            client, client_addr = SERVER.accept() # on getting new connection
            mortal = Mortal(client_addr, client) # create the respective mortal
            mortals.append(mortal)
            print(f"[CONNECTION]{client_addr} connected to server {time.time()}")
            Thread(target=client_communication, args=(mortal,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    # the loop will only break when faced with an exception
    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # open server to listen for connections
    print("[STARTED] Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
