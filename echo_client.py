import socket
import sys


class EchoClient:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = None
        self.socket = None

    def read_port_number(self):
        """
        Read the port number from argument, store it to self.port.
        Exit if invalid argument is provided.
        :return: None
        """
        if len(sys.argv) != 2:
            print("Invalid arguments provided")
            sys.exit(1)

        self.port = int(sys.argv[1])

    def connect_to_port(self):
        """
        Create a socket to try to connect to a specified port,
        store the new socket object to self.socket.
        :return: None
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def receive_and_print_message(self):
        """
        Receive a TCP packet from the server and print
        it out to stdout
        :return: None
        """
        sentence = self.socket.recv(1024)
        print("[Server]", sentence.decode())

    def send_message(self):
        """
        Read messages from stdin, then convert to bytes and
        send out as a TCP packets
        :return: None
        """
        sentence = input()
        self.socket.send(sentence.encode())

    def run_client(self):
        """
        Run the client to send and receive messages with the TCP server
        :return: None
        """
        self.read_port_number()
        self.connect_to_port()
        while True:
            self.send_message()
            self.receive_and_print_message()
        self.socket.close()


if __name__ == "__main__":
    echo_client = EchoClient()
    echo_client.run_client()
