from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:

    HOST = 'localhost'
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name):
        """
        Initiate object and send the name to server
        :param name: str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        recieve_thread = Thread(target=self.receive_message)
        recieve_thread.start()
        self.send_message(name)
        self.lock = Lock()

    def receive_message(self):
        """
        receive messages from server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                print(msg)
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCEPTION]", e)
                break

    def send_message(self, msg):
        """
        send messages to server
        :param msg: str
        :return: None
        """
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print("e")

    def get_messages(self):
        """
        returns a list of string messages
        :return: list[str]
        """
        messages_copy = self.messages[:]

        self.lock.acquire()
        self.messages = []
        self.lock.release()  #for safety in returning messages without another thread updating it

        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")

