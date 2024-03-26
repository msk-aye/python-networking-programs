import socket
import sys
import time
import threading
import os

# Global Variables
INVALID_ARGUMENTS = "Invalid arguments provided\n"
PRINT_RECEIVED = "[Server (%s)] %s\n"
TERMINATED_BY_CLIENT = "[Connection terminated by the client]\n"
TERMINATED_BY_SERVER = "[Connection terminated by the server]\n"
EXIT = "exit"
EMPTY = ""

class ChatClient:
    def __init__(self):
        self.host = "127.0.0.1"
        self.client_name = None
        self.port = None
        self.socket = None

    def get_time(self):
        return time.strftime("%H:%M:%S", time.localtime())

    def read_port_and_client(self):
        """
        Read the port number and client name from arguments, store them to
        self.port and self.client_name.
        Exit with code 1 if invalid argument is provided.
        :return: None
        """
        if len(sys.argv) != 3:
            sys.stdout.write(INVALID_ARGUMENTS)
            os._exit(1)

        self.port = int(sys.argv[1])
        self.client_name = sys.argv[2]

    def connect_to_port(self):
        """
        Create a socket to try to connect to a specified port,
        store the new socket object to self.socket.
        Send the client name to the server when connected
        :return: None
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.send(self.client_name.encode())

    def _receive_and_print_message(self):
        """
        Use a while loop to receive TCP packets from the server and print
        the message out to stdout.
        If the message is "exit", exit the program with code 0
        and print out "[Connection Terminated by the server]" to stdout.
        :return: None
        """
        while True:
            message = self.socket.recv(1024).decode()

            if message == EXIT or not message:
                sys.stdout.write(TERMINATED_BY_SERVER)
                sys.stdout.flush()
                os._exit(0)

            sys.stdout.write(PRINT_RECEIVED % (self.get_time(), message))

    def receive_and_print_message(self):
        """
        Create a new Multithreading
        :return: None
        """
        threading.Thread(target=self._receive_and_print_message).start()

    def send_message(self):
        """
        Use a while loop to read messages from stdin, then convert
        to bytes and send out as a TCP packets.
        If the message is "exit", print out "[Connection Terminated
        by the client]". Close the socket and exit with status 0.
        :return: None
        """
        while True:
            message = input()

            if message == EMPTY:
                continue

            self.socket.send(message.encode())

            if message == EXIT:
                sys.stdout.write(TERMINATED_BY_CLIENT)
                self.socket.close()
                sys.stdout.flush()
                os._exit(0)


    def run_chat_client(self):
        """
        Start the chat client to send and receive messages with the server
        :return: None
        """
        self.read_port_and_client()
        self.connect_to_port()
        self.receive_and_print_message()
        self.send_message()


if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.run_chat_client()
