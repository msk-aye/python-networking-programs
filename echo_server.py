import socket
import sys


class EchoServer:

    def __init__(self):
        self.addr = None
        self.port = None
        self.socket = None
        self.host = "127.0.0.1"
        self.conn = None

    def read_port_number(self):
        """
        Read the port number from argument, store it to self.port.
        Exit with status 1 if invalid argument is provided.
        :return: None
        """
        if len(sys.argv) != 2:
            print("Invalid arguments provided")
            sys.exit(1)

        self.port = int(sys.argv[1])

    def listen_on_port(self):
        """
        Create a socket listens on the specified port.
        Store the socket object to self.socket.
        Store the new accepted connection to self.conn.
        :return: None
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.conn, self.addr = self.socket.accept()
        # print("The server is ready to receive.")

    def receive_message(self):
        """
        Receive a TCP packet from the client.
        :return: None
        :return: the received message
        """
        return self.conn.recv(1024).decode()

    def send_message(self, msg):
        """
        Send the message stored in self.msg back to the client
        :param msg: the message to send to the client
        :return: None
        """
        self.conn.send(msg.encode())

    def echo_messages(self):
        """
        Use a while loop to echo messages back to client
        :return: None
        """
        while True:
            sentence = self.receive_message()
            self.conn.send(sentence.encode())

        self.conn.close()

    def run_echo_server(self):
        """
        Run the echo server to receive and echo back messages
        :return: None
        """
        self.read_port_number()
        self.listen_on_port()
        self.echo_messages()


if __name__ == "__main__":
    echo_server = EchoServer()
    echo_server.run_echo_server()
