from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import time

# Global Constants
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
BUFSIZ = 512

# Global Variables
messages = []

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def receive_message():
    """
    receive messages from server
    :return: None
    """
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            messages.append((msg))
            print(msg)
        except Exception as e:
            print("[EXCEPTION]", e)
            break


def send_message(msg):
    """
    send messages to server
    :param msg: str
    :return: None
    """
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()


recieve_thread = Thread(target=receive_message)
recieve_thread.start()

send_message("pramod")
time.sleep(10)
send_message("hello")
time.sleep(2)
send_message("{quit}")
